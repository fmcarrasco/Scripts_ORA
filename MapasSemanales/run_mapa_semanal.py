import os
import datetime as dt
import numpy as np
import pandas as pd
from pykrige import OrdinaryKriging
import rasterio
import rioxarray
from rasterio import features
from rasterio.mask import mask
import xarray as xr
import matplotlib.pyplot as plt
import time
from colores_ora import *
from funciones_auxiliares import parse_config, agrega_falsos, mapa_revision

start = time.time()
#########################################################
# Parametros de Krigging.
method = 'exponential'
# Exponential model: γ(h) = nugget + (sill - nugget) * (1 - exp(-3h/range))
parameters = {
    'nugget': 15*4.20624827e-10,    # Discontinuity at origin
    'sill': 10*1.05174916e+03,      # Maximum semivariance
    'range': 20*7.78977952e+00      # Practical range (reaches 95% of sill)
}
#########################################################
# Extraemos datos del archivo datos_in.txt

print('############################################')
print('####### Calculo mapas semanales ############')

nml = parse_config('./datos_in.txt')
fecha_i = nml.get('fecha_i')
fecha_f = nml.get('fecha_f')
file_5 = nml.get('file_5')
file_51 = nml.get('file_51')
file_sin_interp = nml.get('file_sin_interp')
provincias_shp = nml.get('provincias_shp')
argentina_shp = nml.get('argentina_shp')
carpeta_salida = nml.get('carpeta_salida')

print('####### Fecha INICIO:', fecha_i, '#####')
print('####### Fecha FIN:', fecha_f, '#####')

# Acomodamos carpeta de salida
f1 = dt.datetime.strptime(fecha_i, '%Y-%m-%d')
f2 = dt.datetime.strptime(fecha_f, '%Y-%m-%d')
c_out = carpeta_salida + f1.strftime('%Y%m%d_') + f2.strftime('%Y%m%d/')
c_out_fig = c_out + 'figuras_test/'
os.makedirs(c_out, exist_ok=True)
os.makedirs(c_out_fig, exist_ok=True)

print('####### Carpeta SALIDA:', c_out, '#####')
#########################################################
# Extension geografica
xmin =-74.0; xmax = -53.5
ymin = -55.2; ymax = -21.7

##########################################################
## COMIENZA EL CODIGO
##
##########################################################

# Guardamos en excel SIN INTERP
df_sin_interp = pd.read_csv(file_sin_interp)
outsininterp = c_out + f1.strftime('%Y%m%d_') + f2.strftime('%Y%m%d_') +'sin_interpolados.xlsx'
df_sin_interp.to_excel(outsininterp, index=False)
print('## $$$ Archivo excel SIN INTERPOLADOS guardado en:', outsininterp)
################################
# Trabajamos con los datos

colvar = ['MaxTmax', 'MinTmin', 'sumPP']
colaa = ['AnomaliaTempDiferencia']
df_5 = pd.read_csv(file_5)
df_51 = pd.read_csv(file_51)

# Agregamos los puntos falsos
df_5 = agrega_falsos(df_5, './datos/FALSOS.txt')
df_51 = agrega_falsos(df_51, './datos/FALSOS.txt')

# ### #### ####### #######

var_semanal = ['MAX', 'MIN', 'MAXEX', 'MINEX', 'PP', 'AA', 'AEX']
columna = ['maxTmax', 'minTmin', 'maxTmax', 'minTmin', 'sumPP', 'AnomaliaTempDiferencia', 'AnomaliaTempDiferencia']
funcion_c = [escala_tmax(), escala_tmin(), escala_tmax_extremas(), escala_tmin_extremas(),
             escala_pp(), escala_aa(), escala_aa_extremas()]

for v1, col, f_c in zip(var_semanal, columna, funcion_c):
    f1_str = f1.strftime('%Y%m%d')
    f2_str = f2.strftime('%Y%m%d')
    print('Variable a interpolar:', v1)
    if (v1 == 'AA') or (v1 == 'AEX'):
        print('Archivo base:', file_51)
        df = df_51.loc[:,['Long', 'Lat', col]]
        df = df.dropna()
    else:
        print('Archivo base:', file_5)
        df = df_5.loc[:,['Long', 'Lat', col]]
        df = df.dropna()
    ##### INTERPOLAMOS CON KRIGGING ######
    x = df['Long'].values % 360.
    y = df['Lat'].values
    z = df[col].values
    OK = OrdinaryKriging(x, y, z, variogram_model=method,
                         variogram_parameters= parameters,
                         verbose=False, enable_plotting=False,
                         coordinates_type='geographic')
    extent=[xmin, xmax, ymax, ymin]
    res_x = 0.059715658
    res_y = 0.059752604
    xrange = np.arange(extent[0], extent[1], res_x if extent[0] < extent[1] else res_x * -1) 
    yrange = np.arange(extent[2], extent[3], res_y if extent[2] < extent[3] else res_y * -1)
    xgrd = np.zeros((yrange.shape[0], xrange.shape[0]))
    ygrd = np.zeros((yrange.shape[0], xrange.shape[0]))
    for i in range(len(xgrd)):
        xgrd[i, :] = xrange
        ygrd[i, :] = np.repeat(yrange[i], len(xrange))
    grid, ss = OK.execute('grid', xrange% 360, yrange)
    if v1 == 'PP':
        grid[grid<0] = 0.
    transform = rasterio.transform.from_bounds(west=xmin, south=ymin, east=xmax, north=ymax, width=grid.shape[1], height=grid.shape[0])
    coords = dict(latitude=yrange, longitude=xrange)
    raster = xr.DataArray(data=grid, coords=coords).astype('float32')\
        .rio.write_transform(transform)\
        .rio.write_crs('epsg:4326')
    f_tiff = c_out + v1 + '_' + f1_str + '_' + f2_str + '.tif'
    raster.rio.to_raster(f_tiff)
    print('## $$$ Archivo raster guardado en:', f_tiff)
    #####
    f_fig = c_out_fig + v1 + '_' + f1_str + '_' + f2_str +'_krigging_python.jpg'
    fig, ax = mapa_revision(argentina_shp, provincias_shp, f_c, df, col, raster)
    plt.savefig(f_fig, dpi=150, bbox_inches='tight')
    print('## $$$ Figura test interpolacion guardada en:', f_fig)


end = time.time()

tiempo = end - start
tiempo_min = np.round(tiempo/60., 2)

print('Tiempo en segundos:', tiempo)
print('Tiempo en minutos:', tiempo_min)
print('########################################')


    
    



