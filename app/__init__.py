from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


App = Flask(__name__)
App.config.from_object(Config)
db = SQLAlchemy(App)
App.debug = True
migrate = Migrate(App, db)
# create the flask_restless API

login = LoginManager(App)
login.login_view = 'login'

# from app import api
from app import admin
from app import routes
from app import error
from app import models
from app.api import bp as api_bp

App.register_blueprint(api_bp, url_prefix='/api')  # register the api_bp



