import os
import base64
from .. import credentials
from imagekitio import ImageKit

def get_imageKit():
    credential = credentials.get_credentials('imagekit')
    return ImageKit(
        public_key = credential['public_key'],
        private_key = credential['private_key'],
        url_endpoint = credential['url_endpoint']
    )

def get_upload_image_result(image_path):
    with open(image_path, mode="rb") as img:
        imgstr = base64.b64encode(img.read())

    return get_imageKit().upload(file=imgstr, file_name=os.path.split(image_path)[-1])

def delete_image(upload_info):
    get_imageKit().delete_file(file_id=upload_info.file_id)
