import re
import os
import shutil
import glob

def parse_config(file_path):
    config = {}
    with open(file_path, 'r') as file:
        for line in file:
            # Use regex to match the variable name and value
            match = re.match(r'(\w+)\s*=\s*"(.*)"', line.strip())
            if match:
                config[match.group(1)] = match.group(2)
    return config


def str_to_bool(s):
    if s == 'True':
         return True
    elif s == 'False':
         return False
    else:
         raise ValueError
    

def copy_shp(archivos, fecha_str, carpeta_out):
    if not archivos:
        print('Lista de Archivos vacia')
        return ''
    for archivo in archivos:
        nombre = os.path.basename(archivo)
        nombre_n = nombre.split('.')[0] + '-' + fecha_str + '.' + nombre.split('.')[1]
        archivo_copy = os.path.join(carpeta_out, nombre_n)
        print('Copiando archivo:', archivo_copy)
        shutil.copy(archivo, archivo_copy)
    print(len(archivos), ' archivos copiados')