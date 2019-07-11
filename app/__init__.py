from flask import Flask
from app.config import Config


from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

App = Flask(__name__)
App.config.from_object(Config)
db = SQLAlchemy(App)
migrate = Migrate(App, db)
login = LoginManager(App)


login.login_view = 'login'
from app import routes
from app import error
from app import models

