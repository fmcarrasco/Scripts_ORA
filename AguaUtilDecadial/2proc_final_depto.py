'''
Este script genera el resumen para cada departamento. Es un excel que es posible
cargar a ARCGis para mapear el promedio de decadico y los dos tipos de anomalia 
implementados.
'''

import datetime as dt
import pandas as pd
import numpy as np
import os
import time

from funciones_auxiliares import calc_AU
from funciones_auxiliares import calc_AnomAU_diff
from funciones_auxiliares import calc_AnomAU_std
from funciones_auxiliares import get_shapefile_AU
from funciones_auxiliares import parse_config


start = time.time()
##################################
# Datos Namelist txt
nml = parse_config('./namelist_agua_util.txt')
guide_file = nml.get('guide_file')
avg_folder = nml.get('avg_folder')
std_folder = nml.get('std_folder')
wrk_folder = nml.get('carpeta_out')

#################################
##### DATOS PARA MODIFICAR ######
fecha = '20251121'
out_folder = 'D:/AguaUtilDecadial/0ResumenDepto_AU/' + fecha + '/'
shapefile_loc='C:/Felix/CAPAS_SIG/otros/dptos_geo.shp'
shape_outfolder = 'D:/AguaUtilDecadial/0ResumenDepto_AU/' + fecha + '/shapefiles/'
#################################


#######################################
## Aca comienza la programacion del codigo
# Creamos la carpeta donde se van a guardar los archivos
os.makedirs(out_folder, exist_ok=True)
os.makedirs(shape_outfolder, exist_ok=True)
# Colocamos los nombres de cultivo y sus equivalentes al archivo salida
guide_clt = ['A1', 'A2', 'G1', 'G2', 'M11', 'M12', 'M21', 'M22', 'S1', 'S2', 'TL', 'TC']
cultivos = ['A11', 'A12', 'G11', 'G12', 'M11', 'M12', 'M21', 'M22', 'S1', 'S2', 'TL', 'TS(TC)']
# Leemos el archivo guia, que luego iremos completando con AU, AnomAUdiff y AnomAUsd
df = pd.read_excel(guide_file, dtype={'LINK':np.str_})
df[guide_clt] = df[guide_clt].astype('float')
nlen = len(df)
fecha_f = dt.datetime.strptime(fecha,'%Y%m%d')
fecha_a = dt.datetime(2000,fecha_f.month,fecha_f.day)  # fecha para abrir datos para anomalias
# Imprimimos algunos datos en pantalla
print('########################################################################')
print('Fecha Resumen AU: ', fecha_f)
print('Fecha Anomalia: ',fecha_a)
print('Carpeta con archivos AU: ', wrk_folder)
print('Archivo guia: ', guide_file)
print('Carpeta con promedios: ', avg_folder)
print('Carpeta con desv. std.: ', std_folder)
print('########################################################################')
#########################################################
############### Resumenes para fecha ####################
#########################################################
print('Generando archivo resumen para AU decadial')
out = np.empty((nlen, len(guide_clt)))
out[:] = -999.
for it, row in df.iterrows():
    if row['Escala'] == 50:
        fdato = wrk_folder + '50_' + fecha_f.strftime('%Y%m%d') + '_resumen_AU.xlsx'
    else:
        fdato = wrk_folder + '500_' + fecha_f.strftime('%Y%m%d') + '_resumen_AU.xlsx'
    aux0 = calc_AU(fdato, row, fecha_f.strftime('%m-%d'))
    out[it, :] = aux0
dfinal = df.copy()
dfinal.loc[:,guide_clt] = out
nout_file = out_folder + 'TablaAU_' + fecha_f.strftime('%Y%m%d') + '.xlsx'
dfinal.to_excel(nout_file, index=False, float_format='%.3f')

# Obtenemos el shapefile
get_shapefile_AU(dfinal, type_AU='AU', shapefile_loc=shapefile_loc, outfolder=shape_outfolder)

#########################################################
############### Resumenes para Anomalia MEAN ############
#########################################################
print('########################################################################')
print('Generando archivo resumen para anomalia AU diff decadial')
df = pd.read_excel(guide_file, dtype={'LINK':np.str_})
df[guide_clt] = df[guide_clt].astype('float')
nlen = len(df)

out = np.empty((nlen, len(guide_clt)))
out[:] = -999.
for it, row in df.iterrows():
    if row['Escala'] == 50:
        fdato = wrk_folder + '50_' + fecha_f.strftime('%Y%m%d') + '_resumen_AU.xlsx'
        fmean = avg_folder + '50_' + fecha_a.strftime('%Y%m%d') + '_resumen_AU_mean.xlsx'
    else:
        fdato = wrk_folder + '500_' + fecha_f.strftime('%Y%m%d') + '_resumen_AU.xlsx'
        fmean = avg_folder + '500_' + fecha_a.strftime('%Y%m%d') + '_resumen_AU_mean.xlsx'
    # Dato de AU
    aux0 = calc_AnomAU_diff(fdato, fmean, row, fecha_f.strftime('%m-%d'))
    out[it, :] = aux0
dfinal = df.copy()
dfinal.loc[:,guide_clt] = out
nout_file = out_folder + 'AU-AAdif_' + fecha_f.strftime('%Y%m%d') + '.xlsx'
dfinal.to_excel(nout_file, index=False, float_format='%.3f')

# Obtenemos el shapefile
get_shapefile_AU(dfinal, type_AU='AU-AAdif', shapefile_loc=shapefile_loc, outfolder=shape_outfolder)

#########################################################
############### Resumenes para Anomalia STD #############
#########################################################
print('########################################################################')
print('Generando archivo resumen para anomalia AU sd decadial')
df = pd.read_excel(guide_file, dtype={'LINK':np.str_})
df[guide_clt] = df[guide_clt].astype('float')
nlen = len(df)

out = np.empty((nlen, len(guide_clt)))
out[:] = -999.
for it, row in df.iterrows():
    if row['Escala'] == 50:
        fdato = wrk_folder + '50_' + fecha_f.strftime('%Y%m%d') + '_resumen_AU.xlsx'
        fmean = avg_folder + '50_' + fecha_a.strftime('%Y%m%d') + '_resumen_AU_mean.xlsx'
        fstd = std_folder + '50_' + fecha_a.strftime('%Y%m%d') + '_resumen_AU_std.xlsx'
    else:
        fdato = wrk_folder + '500_' + fecha_f.strftime('%Y%m%d') + '_resumen_AU.xlsx'
        fmean = avg_folder + '500_' + fecha_a.strftime('%Y%m%d') + '_resumen_AU_mean.xlsx'
        fstd = std_folder + '500_' + fecha_a.strftime('%Y%m%d') + '_resumen_AU_std.xlsx'
    # Dato de AU
    aux0 = calc_AnomAU_std(fdato, fmean, fstd, row, fecha_f.strftime('%m-%d'))
    out[it, :] = aux0
dfinal = df.copy()
dfinal.loc[:,guide_clt] = out
nout_file = out_folder + 'AU-AAsd_' + fecha_f.strftime('%Y%m%d') + '.xlsx'
dfinal.to_excel(nout_file, index=False, float_format='%.3f')

# Obtenemos el shapefile
get_shapefile_AU(dfinal, type_AU='AU-AAsd', shapefile_loc=shapefile_loc, outfolder=shape_outfolder)

#########################
print('########################################################################')
end = time.time()
print('Datos guardados en: ', out_folder)
print('Tiempo de procesamiento: ', np.round((end - start)/60, 2), ' min. ')
print('########################################################################')
