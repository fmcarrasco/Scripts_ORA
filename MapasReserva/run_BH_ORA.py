import os
import shutil
import glob
import time
import pandas as pd
import numpy as np
import datetime as dt
import geopandas as gpd
from funciones_auxiliares import parse_config, str_to_bool, copy_shp

start = time.time()

# Archivo de configuracion de variables
config_file = 'config.txt'

# Leemos el archivo
config = parse_config(config_file)

archivo = config.get('archivo_balance')
fechastr = config.get('fecha')
narchivo = config.get('archivo')
prioridad_m11 = str_to_bool(config.get('prioridad_m11'))
prioridad_m21 = str_to_bool(config.get('prioridad_m21'))
data_folder = config.get('data_folder')
output_folder = config.get('output')
con_fecha = str_to_bool(config.get('con_fecha'))

# Eliminar la carpeta
if os.path.exists(output_folder):
    shutil.rmtree(output_folder)
    print(f"La carpeta {output_folder} ha sido eliminada")
else:
    print("La carpeta no existe")



os.makedirs(output_folder, exist_ok=True)
outf_fecha = output_folder+fechastr+'/'
os.makedirs(outf_fecha, exist_ok=True)


sep = ','
#archivo = carpeta + fechastr + '/' + narchivo
fecha = dt.datetime.strptime(fechastr, '%Y%m%d')

if os.path.isfile(archivo):
    print('##############################################')
else:
    print('### No existe el archivo:', archivo)
    print('### Chequear bien la ruta o los inputs en config.txt')
    exit()

# Que columnas deben quedar en el excel final
columnas_validas = ['centroide', 'P', 'S1', 'S2', 'TL', 'TC', 'M1', 'M2', 'A1', 'A2', 'G1', 'G2']

###############################################
#### CODIGO
###############################################
print('#### Se ordenan las columnas del archivo:', archivo)
print('#### para hacer los mapas de reserva')
print('#### Fecha del mapa de reserva:', fecha.strftime('%d-%m-%Y'))
print('#### Carpeta con shapefile reservas IN:', data_folder)
print('#### Carpeta de salida de shapefiles:', output_folder)
print('#### Estas son las columnas que quedaran al final del script:')
print(columnas_validas)

if sep == ',':
    df1 = pd.read_csv(archivo, sep=',')
else:
    df1 = pd.read_csv(archivo, sep=';', header=0)

# Por determinar porque para este centroide tiene dos sojas y es un centroide de Entre Ríos-->S1-V
# y no de Corrientes que tiene fenologia S1-VII

df1.loc[(df1.centroide == '05meJAI_1'), 'S1-VII'] = np.nan

# Unimos las columnas de SOJA de primera y segunda
df1['S1'] = df1[['S1-III','S1-IV','S1-V','S1-VII']].sum(axis=1, numeric_only=True, min_count=1)
df1['S2'] = df1[['TS(S2)III','TS(S2)IV','TS(S2)V','TS(S2)VI']].sum(axis=1, numeric_only=True, min_count=1)

df1=df1.drop(columns={"S1-III","S1-IV","S1-V","S1-VII","TS(S2)III","TS(S2)IV","TS(S2)V","TS(S2)VI","CoordX","CoordY"})

# Renombramos las columnas de Girasol, Algodon y Trigo tardío
if sep == ';':
    df1.rename(columns={'A1,1': 'A1', 'A1,2': 'A2', 'G1,1': 'G1', 'G1,2': 'G2', 'TS(TC)':'TC'}, inplace=True)
else:
    df1.rename(columns={'A1.1': 'A1', 'A1.2': 'A2', 'G1.1': 'G1', 'G1.2': 'G2', 'TS(TC)':'TC'}, inplace=True)

# Unimos las columnas de Maiz de primera.
# Utilizamos el logical para definir cual tiene prioridad
if sep == ';':
    if prioridad_m11:
        print(u'Prioridad M11 en maíz de primera')
        df1['M1'] = df1['M1,1']
        # Completamos con los datos de M12
        df1.M1.fillna(df1['M1,2'], inplace=True)
    else:
        print(u'Prioridad M12 en maíz de primera')
        df1['M1'] = df1['M1,2']
        # Completamos con los datos de M11
        df1.M1.fillna(df1['M1,1'], inplace=True)
else:
    if prioridad_m11:
        print(u'Prioridad M11 en maíz de primera')
        df1['M1'] = df1['M1.1']
        # Completamos con los datos de M12
        df1.M1.fillna(df1['M1.2'], inplace=True)
    else:
        print(u'Prioridad M12 en maíz de primera')
        df1['M1'] = df1['M1.2']
        # Completamos con los datos de M11
        df1.M1.fillna(df1['M1.1'], inplace=True)

# Unimos las columnas de Maiz de segunda.
# Utilizamos el logical para definir cual tiene prioridad

if sep == ';':
    if prioridad_m21:
        print(u'Prioridad M21 en maíz de primera')
        df1['M2'] = df1['M2,1']
        # Completamos con los datos de M12
        df1.M2.fillna(df1['M2,2'], inplace=True)
    else:
        print(u'Prioridad M22 en maíz de primera')
        df1['M2'] = df1['M2,2']
        # Completamos con los datos de M11
        df1.M2.fillna(df1['M2,1'], inplace=True)
else:
    if prioridad_m21:
        print(u'Prioridad M21 en maíz de primera')
        df1['M2'] = df1['M2.1']
        # Completamos con los datos de M12
        df1.M2.fillna(df1['M2.2'], inplace=True)
    else:
        print(u'Prioridad M22 en maíz de primera')
        df1['M2'] = df1['M2.2']
        # Completamos con los datos de M11
        df1.M2.fillna(df1['M2.1'], inplace=True)

# Unimos las columnas de Trigo de primera TL y TS(TL)

df1['TL'] = df1[['TL','TS(TL)']].sum(axis=1, numeric_only=True, min_count=1)
df1.to_excel(output_folder + 'test_antesdep.xlsx')

# Unimos las columnas de Pradera y Campo Natural
df1['P'] = df1[['P','CN']].sum(axis=1, numeric_only=True, min_count=1)

#################################
# Forma final del DataFrame
#################################
# Nos quedamos con las columnas que nos interesan
df = df1[columnas_validas]

# Agregamos la fila con No Agricola = -2000
nueva_fila = ['NA', -2000, -2000, -2000, -2000, -2000, -2000, -2000, -2000, -2000, -2000, -2000]
new = pd.DataFrame(columns=df.columns, data=[nueva_fila])
# Overwrite original dataframe
df = pd.concat([df, new], axis=0)
df = df.fillna(-1000)
# Usar 'centroide' como INDEX

df = df.set_index('centroide')
df = df.sort_index()

### Guardamos en excel
df.to_excel(output_folder + 'Reservas_al_' + fecha.strftime('%Y%m%d') + '.xlsx')

####################################################
######## Trabajo con los archivos de shape #########
####################################################

"""### RESERVAS"""
print('#### Trabajando y guardando archivos de reserva #####')

reservasshp = os.path.join(data_folder, 'zona_total_mapas_merge13-geo.shp')
reservasgpd = gpd.read_file(reservasshp)
reservasgpd['centroide'] = reservasgpd['Ctrde']
reservasgpd['centroide'].head()
reservasoutgpd = reservasgpd.merge(df, on='centroide')
##### Sin Fecha
output_file = 'RESERVAS.shp'
output_path = os.path.join(output_folder, output_file)
reservasoutgpd.to_file(output_path)
print('### Archivo:', output_path, 'listo.')
##### Hacer copia Con Fecha
archivos_copiar = glob.glob(output_folder+'RESERVAS.*')
copy_shp(archivos_copiar, fecha.strftime('%Y%m%d'), outf_fecha)
# Borrar variables
reservasgpd = None
reservasoutgpd = None



"""### RESERVAS 500"""

R500_201709shp = os.path.join(data_folder, '500_201709.shp')
R500_201709shpIngpd = gpd.read_file(R500_201709shp)
R500_201709shpIngpd['centroide'] = R500_201709shpIngpd['Ctrde_ID']
R500_201709shpIngpd_out = R500_201709shpIngpd.merge(df, on='centroide')
R500_201709shpIngpd_out.head(1)
##### Sin Fecha
output_file = 'RESERVAS_500.shp'
output_path = os.path.join(output_folder, output_file)
R500_201709shpIngpd_out.to_file(output_path)
print('### Archivo:', output_path, 'listo.')
##### Hacer copia Con Fecha
archivos_copiar = glob.glob(output_folder+'RESERVAS_500.*')
copy_shp(archivos_copiar, fecha.strftime('%Y%m%d'), outf_fecha)
# Borrar variables
R500_201709shpIngpd = None
R500_201709shpIngpd_out = None


"""### CBA"""

CBAnewINshp = os.path.join(data_folder, '50-CBAnew-IN.shp')
CBAnewINgpd = gpd.read_file(CBAnewINshp)
CBAnewINgpd['centroide'] = CBAnewINgpd['nom_ctdre']
CBAnewINgpd['centroide'].head(1)
CBAnewINgpd_out = CBAnewINgpd.merge(df, on='centroide')
##### Con Fecha
output_file = '50-CBAnew-OUT.shp'
output_path = os.path.join(output_folder, output_file)
CBAnewINgpd_out.to_file(output_path)
print('### Archivo:', output_path, 'listo.')
##### Hacer copia Con Fecha
archivos_copiar = glob.glob(output_folder+'50-CBAnew-OUT.*')
copy_shp(archivos_copiar, fecha.strftime('%Y%m%d'), outf_fecha)
# Borrar variable
CBAnewINgpd = None
CBAnewINgpd_out = None

"""### CORRIENTES"""

CORRIENTESINshp = os.path.join(data_folder, '50-CORRIENTES-IN.shp')
CORRIENTESINgpd = gpd.read_file(CORRIENTESINshp)
CORRIENTESINgpd['centroide'] = CORRIENTESINgpd['CTRDE']
CORRIENTESINgpd_out = CORRIENTESINgpd.merge(df, on='centroide')
##### Sin Fecha
output_file = '50-CORRIENTES-OUT.shp'
output_path = os.path.join(output_folder, output_file)
CORRIENTESINgpd_out.to_file(output_path)
print('### Archivo:', output_path, 'listo.')
##### Hacer copia Con Fecha
archivos_copiar = glob.glob(output_folder+'50-CORRIENTES-OUT.*')
copy_shp(archivos_copiar, fecha.strftime('%Y%m%d'), outf_fecha)
# Borrar variables
CORRIENTESINgpd = None
CORRIENTESINgpd_out = None


"""### CUENCA del SALADO"""

CuencaSaladoInshp = os.path.join(data_folder, 'P-CN_CuencaSalado.shp')
CuencaSaladoIngpd = gpd.read_file(CuencaSaladoInshp)
CuencaSaladoIngpd['centroide'] = CuencaSaladoIngpd['Centroide']
CuencaSaladoIngpd.drop('Centroide', axis='columns', inplace=True)
CuencaSaladoIngpd_out = CuencaSaladoIngpd.merge(df, on='centroide')
CuencaSaladoIngpd_out.head(1)
##### Sin Fecha
output_file = 'P-CN_Cuenca_Salado.shp'
output_path = os.path.join(output_folder, output_file)
CuencaSaladoIngpd_out.to_file(output_path)
print('### Archivo:', output_path, 'listo.')
##### Hacer copia Con Fecha
archivos_copiar = glob.glob(output_folder+'P-CN_Cuenca_Salado.*')
copy_shp(archivos_copiar, fecha.strftime('%Y%m%d'), outf_fecha)
# Borrar variables
CuencaSaladoIngpd = None
CuencaSaladoIngpd_out = None


end = time.time()
minutos = np.round((end - start)/60., 2)

print(u'##### Tiempo estimado de ejecución:', minutos, ' minutos')