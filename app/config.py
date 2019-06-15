
import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'mysql://bob:secret@192.168.1.7/testF'  #connection to mysql db
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMINS = ['ahmnouira@gmail.com']
    






