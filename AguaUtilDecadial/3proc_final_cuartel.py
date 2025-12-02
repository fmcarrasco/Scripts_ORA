'''
Este script genera el resumen para cada departamento. Es un excel que es posible
cargar a ARCGis/QGis para mapear el promedio de decadico y los dos tipos de anomalia 
implementados.
'''

import datetime as dt
import pandas as pd
import numpy as np
import os
import time


def change_col_clt(df):
    guide_clt = ['M11', 'M12', 'M21', 'S1', 'S2']
    cultivos = ['M11', 'M12', 'M21', 'S1', 'S2']
    df0 = df.copy()
    for clt0, clt1 in zip(cultivos, guide_clt):
        df0.loc[df.Cultivo == clt0,'Cultivo'] = clt1
    return df0

def calc_AU_cuartel(fdato, fecha):
    df0 = pd.read_excel(fdato, index_col='Fecha', usecols=['Fecha', 'AU_WGT'])
    df0.loc[fecha,:].to_numpy()[0]
    return df0.loc[fecha,:].to_numpy()[0]
    
def check_not_val(narray, Se1, m_d):
    guide_clt = ['M11', 'M12', 'M21', 'S1', 'S2']
    # Chequeamos si se hace el cultivo en la decada
    ind_clt = pd.read_csv('./clt_indicador.csv', sep=';', index_col='clt_c')
    se_hace = ind_clt.loc[guide_clt, m_d].to_numpy()
    if np.sum(se_hace == 0) > 0:
        icult = se_hace == 0
        narray[icult] = -998
    # Chequeamos si el cultivo se hace en el departamento
    or_val = Se1[guide_clt].to_numpy()
    if np.sum(or_val == -999) > 0:
        isehace = or_val == -999
        narray[isehace] = -999
    return narray

    
#######################################################################

start = time.time()
##################################
# Datos para modificar

fecha = '2025-11-01'
guide_file = 'c:/Felix/ORA/python_scripts/AguaUtil_operativo/archivos_guia/Cuartel_archivo_guia.xlsx'
#'D:/python/AguaUtil/HistDepartamento/2000-2020/mean/'
wrk_folder = 'c:/Felix/ORA/python_scripts/AguaUtil_operativo/out/'
#'D:/python/AguaUtil/out/'
out_folder = wrk_folder + '0ResumenDepto_AU/'
cuartel_folder = wrk_folder + 'cuartel_50_20251101_20251117/'
out_folder = 'C:/Felix/ORA/web_actualizaciones/AU-distritos/' + '2025-2026/'
#######################################
## Aca comienza la programacion del codigo
# Creamos la carpeta donde se van a guardar los archivos
os.makedirs(out_folder, exist_ok=True)
# Colocamos los nombres de cultivo y sus equivalentes al archivo salida
guide_clt = ['M11', 'M12', 'M21', 'S1', 'S2']
cultivos = ['M11', 'M12', 'M21', 'S1', 'S2']
# Leemos el archivo guia, que luego iremos completando con AU
df = pd.read_excel(guide_file, dtype={'CUARTEL':np.str_})
nlen = len(df)
fecha_f = dt.datetime.strptime(fecha,'%Y-%m-%d')
# Imprimimos algunos datos en pantalla
print('########################################################################')
print('Fecha Resumen AU-Cuartel: ', fecha_f)
print('Carpeta con archivos AU-Cuartel: ', wrk_folder)
print('Archivo guia: ', guide_file)
print('########################################################################')
#########################################################
############### Resumenes para fecha ####################
#########################################################
print('Generando archivo resumen para AU por CUARTEL')
out = np.empty((nlen, len(guide_clt)))
print(out.shape)
out[:] = -999.
print(df)
for it, row in df.iterrows():
    #print(it, row)
    cuartel = row['CUARTEL']
    prov = row['PROVINCIA']
    dpto = row['DPTO']
    for col, cultivo in enumerate(['M11', 'M12', 'M21', 'S1', 'S2']):
        fdato = cuartel_folder + cuartel + '_' + prov + '-' + dpto + '_' + cultivo + '.xlsx'
        if os.path.exists(fdato):
            aux0 = calc_AU_cuartel(fdato, fecha)
            #print(aux0)
        else:
            continue
        out[it, col] = aux0
    out[it,:] = check_not_val(out[it, :], row, fecha_f.strftime('%m-%d'))
dfinal = df.copy()
dfinal.loc[:, guide_clt] = out


#nout_file = out_folder + 'AU-' + fecha_f.strftime('%Y%m%d') + '.xlsx'
#dfinal.to_excel(nout_file, index=False, float_format="%.1f")

##### HTML #############

nout_file = out_folder + 'AU-' + fecha_f.strftime('%Y%m%d') + '.html'
# Set the max_colwidth option to None
pd.set_option('display.max_colwidth', None)
tyled_df = df.style.set_table_styles([
dict(selector='th', props=[('text-align', 'center')]) # Center headers
]).set_properties(
    subset=['PROVINCIA', 'DEPTO', 'CUARTEL'], **{'text-align': 'left'} # Left align 'Product' column
    ).set_properties(
        subset=['M11', 'M12', 'M21', 'S1', 'S2'], **{'text-align': 'right'} # Right align 'Price' and 'Quantity'
        )
dfinal.to_html(nout_file, index=False, float_format="%.2f", justify='center')
print('Archivo guardado:', nout_file)

#########################
print('########################################################################')
end = time.time()
print('Datos guardados en: ', out_folder)
print('Tiempo de procesamiento: ', np.round((end - start)/60, 2), ' min. ')
print('########################################################################')
