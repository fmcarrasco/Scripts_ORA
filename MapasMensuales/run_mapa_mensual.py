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
import sys
sys.path.append('../MapasSemanales/')
from colores_ora import *
from funciones_auxiliares_mensuales import parse_config, mapa_revision
from funciones_auxiliares_mensuales import agrega_falsos_palmer, agrega_falsos


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
f_palmer = nml.get('f_palmer')
f_aapp = nml.get('f_aapp')
provincias_shp = nml.get('provincias_shp')
argentina_shp = nml.get('argentina_shp')
carpeta_salida = nml.get('carpeta_salida')

print('####### Fecha INICIO:', fecha_i, '#####')
print('####### Fecha FIN:', fecha_f, '#####')

# Acomodamos carpeta de salida
f1 = dt.datetime.strptime(fecha_i, '%Y-%m-%d')
f2 = dt.datetime.strptime(fecha_f, '%Y-%m-%d')
c_out = carpeta_salida + f1.strftime('%Y%m/')
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

# Trabajamos con los datos
df_palmer = pd.read_csv(f_palmer)
df_aapp = pd.read_csv(f_aapp)

# Agregamos los puntos falsos
df_palmer = agrega_falsos_palmer(df_palmer, './datos/FALSOS_palmer.txt')
df_aapp = agrega_falsos(df_aapp, './datos/FALSOS.txt')

# ### #### ####### #######
datos = [df_palmer, df_aapp]
var_semanal = ['Palmer', 'AAPP']
columna = ['Z', 'Diferencia']
funcion_c = [escala_palmer(), escala_aa_pp()]

for df, v1, col, f_c in zip(datos, var_semanal, columna, funcion_c):
    f1_str = f1.strftime('%Y%m%d')
    f2_str = f2.strftime('%Y%m%d')
    print('Variable a interpolar:', v1)
    df = df.loc[:,['Long', 'Lat', col]]
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


    
    



