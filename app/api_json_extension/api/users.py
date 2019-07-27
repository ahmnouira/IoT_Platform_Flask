from app.api import api
from flask import jsonify, request
from app.models import User, Cards
from flask import url_for
from app import db
from app.api.error import bad_request
from .auth import auth


@api.route('/users/<int:id>/', methods=['GET', 'POST'])
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())


@api.route('/users/', methods=['GET', 'POST', 'PUT'])
#@auth.login_required
def get_users():
    page= request.args.get('page', 1 , type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    return jsonify(data)


@api.route('/users/<int:id>/cards/', methods=['GET', 'POST'])
def get_user_cards(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(user.cards, page, per_page, 'api.get_user_cards', id=id) # cards is relationship
    return jsonify(data)


@api.route('/users/', methods=['POST'])   # create user
def create_user():
    data = request.get_json() or {} # request.get_json() extract the JSON from the request and return it as python structure
    # ensure that I've got all the information
    if 'firstname' not in data or 'lastname ' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include firstname, lastname, email, password') # return error to client
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email ! ')
    user = User()
    user.form_dict(data, new_user=True)  # new_user: to accepts the password filed
    db.session.add(user)
    db.seesion.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response


@api.route('/users/<int:id>/', methods=['GET', 'POST', 'PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json() or {}

    if 'email' in data and data['email'] != user.email and \
            User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user.form_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())
