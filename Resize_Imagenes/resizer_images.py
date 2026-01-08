from PIL import Image
import os
import glob

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


def resize_images(input_folder, output_folder, target_size=(541, 368)):
    """
    Redimensiona todas las imágenes en una carpeta
    
    Args:
        input_folder (str): Carpeta de origen
        output_folder (str): Carpeta de destino
        target_size (tuple): Tamaño objetivo (ancho, alto)
    """
    
    # Crear carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Formatos de imagen soportados
    extensions = ('*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', '*.webp')
    
    for extension in extensions:
        # Buscar todas las imágenes con la extensión
        for image_path in glob.glob(os.path.join(input_folder, extension)):
            try:
                # Abrir imagen
                with Image.open(image_path) as img:
                    # Redimensionar manteniendo relación de aspecto
                    img_resized = img.resize(target_size, Image.LANCZOS)
                    
                    # Guardar imagen redimensionada
                    filename = os.path.basename(image_path)
                    output_path = os.path.join(output_folder, filename)
                    img_resized.save(output_path)
                    
                    print(f"Imagen redimensionada: {filename}")
                    
            except Exception as e:
                print(f"Error procesando {image_path}: {e}")
                
                
                
# Configuración
nml = parse_config('./config_file.txt')
input_folder = nml.get('input_folder')
output_folder = nml.get('output_folder')
tipo = nml.get('tipo')

os.makedirs(output_folder, exist_ok=True)
if tipo == 'BalanceHidrico':
    target_size = (541, 368)  # Tu tamaño objetivo
elif tipo == 'MapasSemanales':
    target_size = (510, 660)  # Tu tamaño objetivo
else:
    print('No existe ese tipo de imagen.')
    print('Actualmente las opciones son:')
    print('# - BalanceHidrico --> Seguimiento BH por estacion')
    print('# - MapasSemanales --> Resize de imagen para mapa semanal')
    print('########### FIN ###########')
    exit()


resize_images(input_folder, output_folder, target_size)


