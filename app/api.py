
# api using flask_restless ?

from flask_restless import APIManager  # APIManger allow to creat RESTfull endpoints for SQLAlchemy model
from app import db, App
from app.models import User, Cards, Dht11, Gaz

api = APIManager(App, flask_sqlalchemy_db=db)
api.create_api(User, collection_name='users', methods=['GET', 'POST', 'PUT'])
api.create_api(Cards, collection_name='cards', methods=['GET', 'POST', 'PUT'])
api.create_api(Dht11, collection_name='dht11', methods=['GET', 'POST', 'PUT'])



