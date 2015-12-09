"""
This module provides functions that are commonly used by various
members of the friends.py module
"""
import flask
from werkzeug.exceptions import BadRequest

def json_payload(request: flask.request) -> dict:
    """
    Verify that a flask.request object has a JSON payload and
    that it does not contain syntax errors.

    Args:
        request (flask.request): A request object that you want to
            verify has a valid JSON payload.

    Raises:
        ValueError: If the incoming request object is either missing
    """

    try:
        request_payload = request.get_json()
    except BadRequest:
        raise ValueError(
            "JSON payload contains syntax errors. Please fix and try again.")
    else:
        if request_payload is None:
            raise ValueError(
                "No JSON payload present. Make sure that "
                "the appropriate 'content-type' header is included "
                "in your request.")

        required_elements = {"id", "firstName", "lastName", "telephone",
                             "email", "notes"}

        if not required_elements.issubset(request_payload.keys()):
            response = "Missing required payload elements. The following elements are required: {}".format(
                            required_elements.difference(request_payload.keys()))
            raise ValueError(response)