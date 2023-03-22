from flask import Blueprint, request, jsonify
from middlewares.return_json import returns_json
import traceback
from utils.es_utils import insert_into_es
from utils.es_utils import get_last_date

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


@cam_blueprint.route('/last-date/', methods=["GET"])
def get_last_day_es():
    data = {'last_date': None}
    try:
        campaign_id = request.args['campaign_id']
        last_date = get_last_date(campaign_id=campaign_id)
        data['last_date'] = str(last_date) if last_date else None
    except Exception:
        traceback.print_exc()
    return jsonify(data)


@cam_blueprint.route('/healthcheck/ping/', methods=["GET"])
@returns_json
def health_check_status():
    return {"status": "OK"}
