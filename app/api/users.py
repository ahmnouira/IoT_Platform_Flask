from app.api import bp


@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    pass


@bp.route('/users', methods = ['GET'])
def get_users():
    pass

@bp.route('/users/<int:id>/cards', methods=['GET'])
def get_cards(id):
    pass

@bp.route('/users/<int:id>', methods=['POT']) # create user
def create_user():
    pass

@bp.route('/users/<int:id>', methods=['PUT']) # update users
def update_user(id):
    pass
