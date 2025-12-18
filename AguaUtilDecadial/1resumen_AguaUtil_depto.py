import os
import pandas as pd
import numpy as np
import datetime as dt
import time
from funciones_auxiliares import parse_config

def get_xlsfile_data(n_file):
    """
    Extrae provincia, departamento, cultivo del nombre de archivo
    """
    diccionario = {}
    lst = n_file.split('.')[0]
    diccionario['Prov'] = lst.split('_')[0].split('-')[0]
    diccionario['Dpto'] = lst.split('_')[0].split('-')[1]
    diccionario['clt'] = lst.split('_')[1]
    return diccionario

#####################################################################
##################### ACA COMIENZA SCRIPT  ########################
#####################################################################
# Datos Namelist txt
nml = parse_config('./namelist_agua_util.txt')
ret_folder = nml.get('carpeta_ret')
ret_f50 = nml.get('archivo_ret_50')
ret_f500 = nml.get('archivo_ret_500')
out_folder = nml.get('carpeta_out')
##################
opcion = 0 # 0: Toma el ultimo dato; 1: toma el dato de fecha dado
fecha_c = dt.datetime(2024, 4, 11)
c_carpeta = '_20251121_20251216/'
# Carpeta salida x Dpto y Cultivo
resumen_por = 'departamento'
p_out = out_folder
# ---- Cambiar para la corrida
for resol in ['50', '500']:
    
    print('### --- Trabajando por DEPARTAMENTO --- ###')
    print('### --- Resolucion: ', resol, ' --- ###')
    ipath = p_out + resol + c_carpeta
    print('Trabajando en la carpeta:', ipath)
    if opcion == 1:
        print('### --- Opcion: ', opcion, ' para la fecha: ', fecha_c.strftime('%Y-%m-%d'),' --- ###')
    else:
        print('### --- Opcion: ', opcion, u' para última fecha disponible --- ###')
# --------------------- Start Code ---------------------------------------
    if resol == '500':
        print('Resolucion: 500; Reticula: ' + ret_folder + ret_f500)
        dp_file = ret_folder + ret_f500  # cambiar si resol = 500
    elif resol == '50':
        print('Resolucion: 50; Reticula: ' + ret_folder + ret_f50)
        dp_file = ret_folder + ret_f50  # cambiar si resol = 500
    lfiles = [i for i in os.listdir(ipath) if os.path.isfile(os.path.join(ipath, i))]
    dp = pd.read_csv(dp_file, sep=';', encoding='ISO-8859-1')
    resumen = pd.DataFrame(columns=['Fecha', 'Prov', 'Depto', 'LINK', 'AU_WGT', 'Cultivo'])
    ############
    start_time = time.time()
    print('Trabajando en: ' + str(len(lfiles)) + ' archivos')
    for nfile in lfiles:
        dlt = get_xlsfile_data(nfile)
        df = pd.read_excel(ipath + nfile)
        if opcion == 0:
            ul = df[['Fecha', 'AU_WGT']].iloc[-1]
            fecha = ul.Fecha
        elif opcion == 1:
            ul = df[df['Fecha'] == fecha_c].iloc[0]
            fecha = ul.Fecha

    # ############################
        a = dp[np.logical_and(dp['PROVINCIA'] == dlt['Prov'],
                              dp['DEPTO'] == dlt['Dpto'])]
        link = a['LINK'].iloc[0]
        b = {'Fecha':fecha, 'Prov':dlt['Prov'], 'Depto':dlt['Dpto'], 'LINK':link,
             'AU_WGT':ul.AU_WGT, 'Cultivo':dlt['clt'] }
        if resumen.empty:
            resumen = pd.DataFrame([b])
        else:
            resumen = pd.concat([resumen, pd.DataFrame([b])], ignore_index=True)
        
# Guardamos excel con resultado
    print('### --- Guardamos variables --- ###')
    nombre = p_out + resol + '_' + fecha.strftime('%Y%m%d') + '_resumen_AU.xlsx'
    resumen.to_excel(nombre, sheet_name='Resumen Agua Util')
#
print('Tiempo de demora del script:')
print("--- %s seconds ---" % np.round((time.time() - start_time),2))
