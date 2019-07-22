# for error handling
from flask import jsonify # jsonify return a flask response object with a default status code of 200
from werkzeug.http import HTTP_STATUS_CODES # dictonary provides a short descriptive name of each HTTP status code


def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


def bad_response(message): # 400 when the client sends a request that has invalid data on it
    return error_response(400, message)



