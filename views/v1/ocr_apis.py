from flask import Blueprint, request
from middlewares.return_json import returns_json
from data.image_extract import read_image
import traceback

ocr_blueprint = Blueprint('ocr_blueprint', __name__)


@ocr_blueprint.route('/healthcheck/ping/', methods=["GET"])
@returns_json
def health_check_status():
    return {"status": "OK"}


@ocr_blueprint.route('/real-time-validate/', methods=["POST"])
@returns_json
def approve_screenshot():
    try:
        data = {
        'img_link' : request.json['img_url'],
        'user_id' : request.json['user_id'],
        'campaign_id' : int(request.json['campaign_id']),
        'product_url' : request.json.get('product_url', ''),
        'real_time': True
        }
        ex_da = {}
        platform = request.json.get('platform')
        if platform == 'amazon':
            ex_da = read_image(**data)
        else:
            return {'msg': 'platforn not recognised'}
        return ex_da
    except Exception:
        traceback.print_exc()
    return {'msg': 'internal server error'}
    