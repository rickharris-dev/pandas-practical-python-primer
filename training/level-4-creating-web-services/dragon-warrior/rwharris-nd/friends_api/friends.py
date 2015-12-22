from flask import Flask, jsonify, make_response, request, Response, g
from werkzeug.exceptions import BadRequest

from friends_api.datastore import Datastore

app = Flask(__name__)

@app.before_request
def connect_to_datastore():
    """
    Establish a connection to the datastore and store it on the 'g' object.
    """
    g.datastore = Datastore()

@app.teardown_request
def disconnect_from_datastore(exception):
    """
    Close the connection to the datastore.
    """
    del g.datastore

@app.route('/api/v1/friends', methods=['GET'])
def friends() -> Response:
    """
    Return a representation of the collection of friend resources.

    Returns:
        A flask.Response object.
    """
    return jsonify({"friends": g.datastore.friends()})


@app.route('/api/v1/friends/<id>', methods=['GET'])
def specific_friend(id: str) -> Response:
    """
    Return a representation of a specific friend resource.

    Args:
        id: The unique ID value of a given friend.

    Returns:
        A flask.Response object.
    """

    try:
        matched_friend = g.datastore.friend(id)
    except ValueError as error:
        error_response = make_response(
            jsonify({"error": str(error)}), 404)
        return error_response
    else:
        return jsonify(matched_friend)


@app.route('/api/v1/friends', methods=['POST'])
def create_friend() -> Response:
    """
    Create a new friend resource.

    Utilize a JSON representation/payload in the request object to
    create a new friend resource.

    Returns:
        A flask.Response object.
    """
    try:
        request_payload = request.get_json()
    except BadRequest as error:
        response = make_response(
            jsonify({"error": str(error)}), 400)
        return response

    try:
        g.datastore.create_friend(request_payload)
    except ValueError as error:
        response = make_response(
            jsonify({"error": str(error)}),
            400)
        return response

    response = make_response(
        jsonify({"message": "Friend resource created."}), 201)
    return response


@app.route('/api/v1/friends/<id>', methods=['PATCH'])
def update_friend(id: str) -> Response:
    """
    Update an existing friend resource.

    Utilize a JSON representation/payload in the request object to
    updated an existing friend resource.

    Args:
        id: The unique ID value of a given friend.

    Returns:
        A flask.Response object.
    """
    try:
        request_payload = request.get_json()
    except BadRequest as error:
        response = make_response(
            jsonify({"error": "JSON payload contains syntax errors. "
                              "Please fix and try again."}),
            400)
        return response

    try:
        g.datastore.update_friend(id, request_payload)
    except ValueError as error:
        response = make_response(
            jsonify({"error": str(error)}),
            400)
        return response

    response = make_response(
        jsonify({"message": "Friend resource updated."}), 201)
    return response

@app.route('/api/v1/friends/<id>', methods=['DELETE'])
def destroy_friend(id: str) -> Response:
    """
    Delete a specific friend resource or return an error.

    Args:
        id: The unique ID value of a given friend.

    Returns:
        A flask.Response object.
    """
    try:
        g.datastore.destroy_friend(id)
    except ValueError as error:
        response = make_response(jsonify({"error": str(error)}), 400)
        return response

    return jsonify({"message": "Friend resource removed."})