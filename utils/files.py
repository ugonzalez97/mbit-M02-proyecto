import os
import base64

def get_image_size(file_path):
    try:
        file_size = os.path.getsize(file_path)
        return file_size / 1024
    except OSError:
        raise Exception(f"No se pudo obtener el tamaño del archivo: {file_path}")

def save_image_from_base64(image_data, image_path):
    if not os.path.isdir('data/'):
        os.mkdir('data/')
    with open(image_path, 'wb') as file:
        file.write(base64.b64decode(image_data))

def get_image_base64(file_path):
    with open(file_path, 'rb') as file:
        image_bytes = file.read()
        image_base64 = base64.b64encode(image_bytes)
        return image_base64.decode('utf-8')

