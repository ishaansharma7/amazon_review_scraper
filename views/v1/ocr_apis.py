from flask import Blueprint, request
from middlewares.return_json import returns_json
from data.image_extract import read_image
import traceback

ocr_blueprint = Blueprint('ocr_blueprint', __name__)


@ocr_blueprint.route('/approve-screenshot/', methods=["POST"])
@returns_json
def approve_screenshot():
    try:
        pass
        # read_image()
    except Exception:
        traceback.print_exc()
    return {'status': 'worked'}
    