
import os
from app.networks import get_ip


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    #connection to mysql db
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://bob:secret@{}/testF'.format(get_ip())      
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.environ.get('DEBUG') or True
    TESTING = True
    ADMINS = ['ahmnouira@gmail.com']
    ADMIN_PASSWORD = 'aze'
    ROLES = ["admin", "user"]

    ## mySQL database configuration
    MYSQL_RANDOM_ROOT_PASSWORD=os.environ.get('MYSQL_RANDOM_ROOT_PASSWORD') or "yes"
    MYSQL_DATABASE=os.environ.get('MYSQL_DATABASE') or "iot_platform_db"
    MYSQL_USER=os.environ.get('MYSQL_USER') or "iot_platform"
    MYSQL_PASSWORD=os.environ.get('MYSQL_PASSWORD') or "secret"






