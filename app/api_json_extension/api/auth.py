from flask_httpauth import HTTPBasicAuth
from app.models import User
from flask import g
from flask_login import current_user
from .error import unauthorized, forbidden
from app.api import api

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email, password):
    if email=='':
        return False
    user = User.query.filter_by(email = email).first()
    if not user:
        return False
    g.current_user = user
    return user.check_password(password)


@auth.error_handler
def auth_error():
    return unauthorized('Invalid Credentials')


#@api.before_request
#@auth.login_required
#def before_request():
  #  if not g.current_user.is_anonymous:
   #     return forbidden('Unconfirmed account!!!!!!')
