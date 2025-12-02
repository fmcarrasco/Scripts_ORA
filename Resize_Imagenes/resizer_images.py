from PIL import Image
import os
import glob


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
input_folder = "origen"  # Cambiar por tu ruta
output_folder = "destino"  # Cambiar por tu ruta
target_size = (541, 368)  # Tu tamaño objetivo


resize_images(input_folder, output_folder, target_size)


