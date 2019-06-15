from flask import Flask
from app.config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
App = Flask(__name__)
App.config.from_object(Config)
db = SQLAlchemy(App)
migrate = Migrate(App, db)

from app import routes
from app import error
from app import models

