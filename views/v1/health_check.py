from flask import Flask, render_template, redirect, jsonify, current_app, request, session, g, abort, Blueprint, flash, url_for
from middlewares.return_json import returns_json

health_check_blueprint = Blueprint('health_check_blueprint', __name__)


@health_check_blueprint.route('/v1/healthcheck/ping/', methods=["GET"])
@returns_json
def health_check_status():
    return {"status": "OK"}

