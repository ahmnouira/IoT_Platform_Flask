
import os
from app.networks import get_ip


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://bob:secret@{}/testF'.format(get_ip())  #connection to mysql db
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMINS = ['ahmnouira@gmail.com']
    ADMIN_PASSWORD = 'aze'
    ROLES = ["admin", "user"]
    






