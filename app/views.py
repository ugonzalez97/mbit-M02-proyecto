from ...import controller
from flask import Blueprint, request

bp = Blueprint('pictures', __name__, url_prefix='/')

@bp.post("/image")
def post_image():
    if not request.is_json:
        return "Body must be a json", 400
    
    min_confidence = int(request.args.get("min_confidence", 80))
    return controller.process_image(request.json['data'], min_confidence)

@bp.get("/image/<image_id>")
def get_image(image_id):
    if not image_id:
        return []
    
    return controller.get_image(image_id)

@bp.get("/images")
def get_images():
    min_date = request.args.get("min_date", None)
    max_date = request.args.get("max_date", None)

    tags = request.args.get("tags", '').split(',')
    if not tags:
        return []

    return controller.get_images(min_date, max_date, tags)

@bp.get("/tags")
def get_tags():
    pass
