import uuid
from . import models
from ..utils import files
from datetime import datetime
from ..utils import validations
from .utils.ext_apis import imagekit, imagga

def process_image(encoded_image, min_confidence):
    # Generar un ID único para la imagen
    image_id = str(uuid.uuid4())

    # Crear el nombre del archivo de imagen
    image_filename = image_id + '.jpg'

    # Obtener la fecha y hora actual en formato YYYY-MM-DD HH:MM:SS
    formatted_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Construir la ruta completa de la imagen
    image_path = 'data/' + image_filename

    # Guardar la imagen decodificada en el sistema de archivos
    files.save_image_from_base64(encoded_image, image_path)

    # Obtener la URL pública de la imagen subida
    image_data = imagekit.get_upload_image_result(image_path)

    # Obtener las etiquetas de la imagen usando Imagga API
    tags = imagga.get_image_tags(image_data.url, min_confidence)

    # Borrar la imagen de imagekit
    imagekit.delete_image(image_data)

    # Guardar la información de la imagen en la base de datos
    models.save_image(image_id, image_path, formatted_datetime, tags)

    # Construir la respuesta JSON
    response = {
        'id': image_id,
        'size': files.get_image_size(image_path),
        'date': formatted_datetime,
        'tags': tags,
        'data': encoded_image
    }

    return response

def get_image(image_id):
    image = models.get_image(image_id)

    if image is None:
        return {'error': 'Imagen no encontrada'}, 404

    size = files.get_image_size(image['path'])
    encoded_image = files.get_image_base64(image['path'])

    response = {
        'id': image_id,
        'size': size,
        'date': image['date'],
        'tags': image['tags'],
        'data': encoded_image[:50]
    }

    return response

def get_images(min_date, max_date, tags):
    if not validations.dates_are_valid(min_date, max_date):
        raise Exception('Given dates do not match required format (YYYY-MM-DD HH:MM:SS)')
    
    res = models.get_images(min_date, max_date, tags)
    images = []
    for image in res:
        image_id, path, date, tags = image
        size_kb = files.get_image_size(path)
        if size_kb is not None:
            tag_objects = []
            print(tags)
            for tag in tags:
                tag_name = list(tag.keys())[0]
                confidence = list(tag.values())[0]
                tag_objects.append({"tag": tag_name, "confidence": confidence})
            image_with_size = {
                "id": image_id,
                "size": size_kb,
                "date": date,
                "tags": tag_objects
            }
            images.append(image_with_size)
    return images
