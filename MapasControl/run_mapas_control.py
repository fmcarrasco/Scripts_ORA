import numpy as np
import pandas as pd
import os
import shutil
import time
import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from colores_ora import escala_pp, escala_tmax, escala_tmin
from colores_ora import escala_mapa_control_extr_pp, escala_mapa_control_extr_tmax
from colores_ora import escala_mapa_control_extr_tmin

start = time.time()
#######################################################
def parse_config(file_path):
    import re
    config = {}
    with open(file_path, 'r') as file:
        for line in file:
            # Use regex to match the variable name and value
            match = re.match(r'(\w+)\s*=\s*"(.*)"', line.strip())
            if match:
                config[match.group(1)] = match.group(2)
    return config


def chequea_extremos(lons, lats, dato, prefijo):
    print('Chequeando Extremos!')
    hay_extr = False
    plot_var = {}
    if prefijo == 'pp':
        if (np.any(dato, where=dato>=250)):
            print('Hay extremos de PP')
            hay_extr = True
            plot_var['x'] = lons[dato>=250]
            plot_var['y'] = lats[dato>=250]
            plot_var['dato'] = dato[dato>=250]
    elif prefijo == 'tmax':
        if ((dato<5).any()) or ((dato>=45).any()):
            print('Hay extremos de Tmax')
            hay_extr = True
            i_extr = np.logical_or(dato<5, dato>=45)
            plot_var['x'] = lons[i_extr]
            plot_var['y'] = lats[i_extr]
            plot_var['dato'] = dato[i_extr]
    elif prefijo == 'tmin':
        if ((dato<-15).any()) or ((dato>=25).any()):
            print('Hay extremos de Tmin')
            hay_extr = True
            i_extr = np.logical_or(dato<-15, dato>=25)
            plot_var['x'] = lons[i_extr]
            plot_var['y'] = lats[i_extr]
            plot_var['dato'] = dato[i_extr]

    return hay_extr, plot_var

######################################
###### DATOS PARA QUE FUNCIONE
######################################
nml = parse_config('./config_mapas_control.txt')
archivo_in = nml.get('archivo_in')  #'C:/Felix/Programa_ORA/Salidas/IN.txt'
archivo_out = nml.get('archivo_out')  #'C:/Felix/Programa_ORA/Salidas/OUT.txt'
shape_provincias = nml.get('shape_provincias')  #'C:/Felix/CAPAS_SIG/otros/provincias_geo.shp'
shape_deptos = nml.get('shape_deptos')  #'C:/Felix/CAPAS_SIG/otros/dptos_geo.shp'

print('##### INICIO SCRIPTS MAPAS CONTROL #####')
print('## Archivo IN en:', archivo_in)
print('## Archivo OUT en:', archivo_out)
print('## Shapefile provincias en:', shape_provincias)
print('## Shapefile departamentos en:', shape_deptos)
#######################################




din = pd.read_csv(archivo_in)
din=din.rename(columns = {'sumPP':'pp', 'maxTmax':'tmax', 'minTmin':'tmin'})
dout = pd.read_csv(archivo_out)
dout=dout.rename(columns = {'sumPP':'pp', 'maxTmax':'tmax', 'minTmin':'tmin'})

columnas = ['pp', 'tmax', 'tmin']
funcion_color = [escala_pp, escala_tmax, escala_tmin]
funcion_extr = [escala_mapa_control_extr_pp, escala_mapa_control_extr_tmax, escala_mapa_control_extr_tmin]
# carpeta salida
carpeta_salida = './output/'
if os.path.exists(carpeta_salida):
    shutil.rmtree(carpeta_salida)
    print(f"La carpeta {carpeta_salida} ha sido eliminada")
os.makedirs(carpeta_salida, exist_ok=True)

# Datos para el mapa
argentina_gdf = gpd.read_file(shape_provincias)
argentina_gdf = argentina_gdf.to_crs(4326)
deptos_gdf = gpd.read_file(shape_deptos)

for df, prefijo in zip([din, dout], ['IN', 'OUT']):
    lats = df.Lat.to_numpy()
    lons = df.Long.to_numpy()
    for columna, escala, escala_extr in zip(columnas, funcion_color, funcion_extr):
        print('#### Haciendo el mapa de', columna, prefijo)
        dato = df[columna].to_numpy()
        # 
        xnan = lons[np.isnan(dato)]
        ynan = lats[np.isnan(dato)]
        #
        i_condato = np.logical_not(np.isnan(dato))
        xdato = lons[i_condato].copy()
        ydato = lats[i_condato].copy()
        cdato = dato[i_condato].copy()

        c_pp, cMap, bounds, norm = escala()
        fig = plt.figure(figsize=(15, 10))
        ax = plt.axes(projection=ccrs.PlateCarree())  # Use Lat/Lon projection
        ax.add_geometries(argentina_gdf.geometry, crs=ccrs.PlateCarree(), facecolor='none', edgecolor='black', linewidth=0.6, zorder=0)
        ax.add_geometries(deptos_gdf.geometry, crs=ccrs.PlateCarree(), facecolor='none', edgecolor='gray', linewidth=0.3, zorder=-1)
        scatter_nan = ax.scatter(xnan, ynan, c='black', s=7, transform=ccrs.PlateCarree(), zorder=2)
        scatter_dato = ax.scatter(xdato, ydato, c=cdato, cmap=cMap, norm=norm, s=40,
                                  edgecolors='black', linewidth=0.5, transform=ccrs.PlateCarree(), zorder=3)
        #### Datos Extremos: A REVISAR COMO HACER
        '''
        hay_extr, plot_var = chequea_extremos(xdato, ydato, cdato, columna)
        if hay_extr:
            print(plot_var)
            c_extr, cMap_extr, bounds_extr, norm_extr = escala_extr()
            #ax.plot()
            scatter_extr = ax.scatter(plot_var['x'], plot_var['y'], c=plot_var['dato'], marker='*', s=200,
                                      cmap=cMap_extr, norm=norm_extr, transform=ccrs.PlateCarree(), zorder=5)
        '''
        ax.set_extent([-75, -50, -55, -20], crs=ccrs.PlateCarree())
        plt.savefig(carpeta_salida + prefijo + '_' + columna + '.jpg', bbox_inches='tight')
        plt.close(fig)

print('#### Imagenes guardadas en:', carpeta_salida)
print('######## FIN SCRIPT ########')

end = time.time()
segundos = np.round((end - start), 2)

print(u'##### Tiempo estimado de ejecución:', segundos, 'segundos')

