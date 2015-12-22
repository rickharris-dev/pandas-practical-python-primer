from datetime import date, time
from dateutil.relativedelta import relativedelta
from flask import Flask, jsonify, make_response, request, Response, g
from werkzeug.exceptions import BadRequest

from hd_hours_api.holiday import Holiday
from hd_hours_api.data import Data

app = Flask(__name__)

@app.before_request
def connect_to_holidays():
    g.holidays = Holiday()
    g.data = Data()

@app.teardown_request
def disconnect_from_holidays(exception):
    del g.holidays
    del g.data

@app.route('/api/v1/holidays', methods=['GET'])
def holidays() -> Response:
    return jsonify(g.holidays.get_all_holidays())

@app.route('/api/v1/team_attributes/<team>')
def team_attributes(team:str) -> Response:
    try:
        matched_attributes = g.data.get_attributes(team)
    except ValueError as error:
        error_response = make_response(
            jsonify({"error": str(error)}),404)
        return error_response
    else:
        return jsonify(matched_attributes)

@app.route('/api/v1/team_attribute/<team>/<attribute_name>')
def team_attribute(team:str, attribute_name:str) -> Response:
    try:
        matched_attribute = g.data.get_attribute(team, attribute_name)
    except ValueError as error:
        error_response = make_response(
            jsonify({"error": str(error)}),404)
        return error_response
    else:
        return jsonify(matched_attribute)

@app.route('/api/v1/team_attribute/<team>', methods=['POST'])
def create_attribute(team:str) -> Response:
    try:
        request_payload = request.get_json()
    except BadRequest as error:
        response = make_response(
            jsonify({"error": str(error)}), 400)
        return response

    try:
        g.data.create_attribute(request_payload)
    except ValueError as error:
        response = make_response(
            jsonify({"error": str(error)}), 400)
        return response
    else:
        response = make_response(
            jsonify({"message": "Team attribute created."}), 201)
        return response

@app.route('/api/v1/team_attribute/<id>', methods=['PATCH'])
def update_attribute(id:str) -> Response:
    try:
        request_payload = request.get_json()
    except BadRequest as error:
        response = make_response(
            jsonify({"error": str(error)}), 400)
        return response

    try:
        g.data.update_attribute(id, request_payload)
    except ValueError as error:
        response = make_response(
            jsonify({"error": str(error)}), 400)
        return response
    else:
        response = make_response(
            jsonify({"message": "Team attribute updated."}), 201)
        return response

    time.replace(hour=7,minute=30,tzinfo=time.tzinfo)