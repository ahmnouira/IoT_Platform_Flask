from flask import Flask                     # import Flask
from app.config import Config               # import class Conifg
from flask_sqlalchemy import SQLAlchemy     # import SQLAlchemy
from flask_migrate import Migrate           # import Migrate
from flask_login import LoginManager        # import loginManager
#from flask_restful import Api              # import Api

App = Flask(__name__)                       # create App object
App.config.from_object(Config)              # set configurations of the app from Config
db = SQLAlchemy(App)                        # create database instance
migrate = Migrate(App, db)
#api = Api(App)                              # initize api
login = LoginManager(App)
login.login_view = 'login'

# import models, at the bottom to avoid circulaire depencies importaion
''' use extension for API feature '''

#from app.api import api as api_bp
#App.register_blueprint(api_bp, url_prefix='/api')  # register the api_bp


from app import admin
from app import routes
from app import error
from app import models
from app import api_restfull_extension
from app import mqtt






