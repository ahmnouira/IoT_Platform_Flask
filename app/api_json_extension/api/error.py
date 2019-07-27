# for error handling
from flask import jsonify  # jsonify return a flask response object with a default status code of 200
from werkzeug.http import HTTP_STATUS_CODES  # dictonary provides a short descriptive name of each HTTP status code
from app.api import api
from flask import render_template
from app import App
from flask import request
from app.exceptions import ValidationError


def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


def bad_request(message):  # 400 when the client sends a request that has invalid data on it
    return error_response(400, message)


def wants_json_response():
    return request.accept_mimetypes['application/json'] >= \
        request.accept_mimetypes['text/html']


@api.app_errorhandler(404)
def not_found_error(error):
    if wants_json_response():
        return error_response(404)
    return render_template('404.html'), 404   # render_template  args search in template folder


### like O'relly
def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response



#  METHOD NOT ALLOWED,
def method_not_allowed(message):
    return error_response(405, message)


@api.errorhandler(500)
def internal_error(error):
    if wants_json_response():
        return error_response(500)
    return render_template('500;html'), 500


@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])
