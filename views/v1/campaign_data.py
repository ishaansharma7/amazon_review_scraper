from flask import Blueprint, request
from middlewares.return_json import returns_json
import traceback
from utils.es_utils import insert_into_es
from dateutil.parser import parse

cam_blueprint = Blueprint('cam_blueprint', __name__)


@cam_blueprint.route('/reviews/', methods=["POST"])
@returns_json
def insert_campaign_data():
    try:
        insert_into_es(request.json)
        return {'status': 'inserted data in es'}
    except Exception:
        traceback.print_exc()
    return {'status': 'failed'}
    
@cam_blueprint.route('/healthcheck/ping/', methods=["GET"])
@returns_json
def health_check_status():
    return {"status": "OK"}
