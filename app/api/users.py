from app.api import bp
from flask import jsonify
from app.models import User
@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())


@bp.route('/users', methods=['GET'])
def get_users():
    return jsonify(User.query.all())

@bp.route('/users/<int:id>/cards', methods=['GET'])
def get_cards(id):
    pass

#@bp.route('/users/<int:id>', methods=['POT']) # create user
#def create_user():
 #   pass

#@bp.route('/users/<int:id>', methods=['PUT']) # update users
#def update_user(id):
 #   pass
