
# whats' differnece betwenn flask_restless and restfull

# doc,  flask_restfull: https://flask-restful.readthedocs.io/en/latest/
from flask_restful import Resource       # import Resource class ( define the routing for one or more HTTP )
from app import App, db                   # import App object
from flask_restful import Api, reqparse
from app.models import User, Cards, Dht11
from flask import abort, jsonify, url_for, request
import json
API = Api(App)


class UserAPI(Resource):               # Resource:  User
    parse = reqparse.RequestParser()
    parse.add_argument('first_name', type=str, required=True)
    parse.add_argument('last_name', type=str)
    parse.add_argument('password', type=str, required=True)
    parse.add_argument('email', type=str, required=True)
    parse.add_argument('last_seen', type=str)
    parse.add_argument('nb_cards', type=int)

    @staticmethod
    def get(id=None, page=1):                 # GET
        if not id:
            users = User.query.paginate(page, 10).items
        else:
            users = [User.query.get_or_404(id)]

        response = {}
        for u in users:
            response[u.id] = {
                'first_name': u.firstname,
                'last_name': u.lastname,
                'email': u.email,
                'nb_cards': u.cards.count(),
                'member_since': u.created_timestamp,
                '_links': {
                    'self': url_for('userapi'),
                    'your_cards': '/api/users/{}/cards'.format(u.id)
                    #'your_cards': url_for('api.get_user_cards', id=self.id),
                }

            }
        return jsonify(response)

    def post(self):
        # create a new user
        args = self.parse.parse_args()
        first_name = args['first_name']
        last_name = args['last_name']
        password = args['password']
        email = args['email']
        user = User(firstname=first_name, lastname=last_name, email=email, password=password,  admin=False)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        response = {}
        response[user.id] = {
            'first_name': user.firstname,
            'last_name': user.lastname,
            'email': user.email,
            'nb_cards': user.cards.count(),
            'member_since': user.created_timestamp,
            '_links': {

            }

        }
        return jsonify(response)

    def put(self, id):
        # update a user
        args = self.parse.parse_args()
        first_name = args['first_name']
        last_name = args['last_name']
        email = args['email']
        password = args['password']
        user = User.query.filter_by(id=id).update({
            'firstname': first_name,
            'lastname': last_name,
            'email': email,
            'password': password
        })
        db.session.commit()
        u = User.query.get_or_404(id)
        u.set_password(password)
        response = {}
        response[u.id] = {
            'first_name': u.firstname,
            'last_name': u.lastname,
            'email': u.email,
            'nb_cards': u.cards.count(),
            'member_since': u.created_timestamp,

        }
        return jsonify(response)

    def delete(self, id):
        user = User.query.get_or_404(id)
        user.delete()
        db.session.commit()
        return jsonify({'Response':'Success'})


class UserCardAPI(Resource):

    parse = reqparse.RequestParser()
    parse.add_argument('name', type=str, required=True)
    parse.add_argument('owner', type=str, required=True)
    parse.add_argument('dht11_values', type=str)
    parse.add_argument('gaz_values', type=str)
    parse.add_argument('created', type=str)

    @staticmethod
    def get(id_):  # GET
        user = User.query.get_or_404(id_)
        user_cards = user.cards
        response = {}
        for c in user_cards:
            response[c.id] = {
                'name': c.name,
                'owner': str(User.query.filter_by(id=c.user_id).first().full_name()),
                'owner_email': str(User.query.filter_by(id=c.user_id).first().email),
                'created': c.timestamp,
                'dh11_values': c.dht11_values.count(),
                'gaz_values': c.gaz_values.count(),
                '_links': {
                    'self': '/api/cards/{}/'.format(c.id),
                    'owner_url': '/api/users/{}/'.format(c.user_id),  # user_id
                    # 'dht11_sensor': url_for('api.get_card_dht11', id=self.id)
                }

            }
        return jsonify(response)


class CardsAPI(Resource):

    parse = reqparse.RequestParser()
    parse.add_argument('name', type=str, required=True)
    parse.add_argument('owner_email', type=str, required=True)
    parse.add_argument('dht11_values', type=str)
    parse.add_argument('gaz_values', type=str)
    parse.add_argument('created', type=str)

    @staticmethod
    def get(id=None, page=1):  # GET
        if not id:
            cards = Cards.query.paginate(page, 10).items
        else:
            cards = [Cards.query.get_or_404(id)]

        response = {}
        for c in cards:
            response[c.id] = {
                'name': c.name,
                'owner': str(User.query.filter_by(id=c.user_id).first().full_name()),
                'owner_email': str(User.query.filter_by(id=c.user_id).first().email),
                'created': c.timestamp,
                'dh11_values': c.dht11_values.count(),
                'gaz_values': c.gaz_values.count(),
                '_links': {
                    'self': '/api/cards/{}/'.format(c.id),
                    'owner_url': '/api/users/{}/'.format(c.user_id),  # user_id
                    #'dht11_sensor': url_for('api.get_card_dht11', id=self.id)
                }

             }
        return jsonify(response)

    def post(self):
        # create a new user
        args = self.parse.parse_args()
        name = args['name']
        owner_email = args['owner_email']
        if owner_email:
            u = User.query.filter_by(email=owner_email).first()
        card = Cards(name=name, user_id =u.id)
        db.session.add(card)
        db.session.commit()
        response = {}
        response[card.id] = {
            'name': card.name,
            'owner': str(User.query.filter_by(id=card.user_id).first().full_name()),
            'owner_email': str(User.query.filter_by(id=card.user_id).first().email),
            'created': card.timestamp,
            'dh11_values': card.dht11_values.count(),
            'gaz_values': card.gaz_values.count(),
            '_links': {
                'self': '/api/cards/{}/'.format(card.id),
                'owner_url': '/api/users/{}/'.format(card.user_id),  # user_id
                # 'dht11_sensor': url_for('api.get_card_dht11', id=self.id)
            }
        }
        return jsonify(response)

    def put(self, id):
        # update a user
        args = self.parse.parse_args()
        name = args['name']
        owner = args['owner_email']

        card = Cards.query.filter_by(id=id).update({
            'name': name,
            'owner_email': owner,

        })
        db.session.commit()
        c = Cards.query.get_or_404(id)
        response = {}
        response[c.id] = {
            'name': card.name,
            'owner': str(User.query.filter_by(id=card.user_id).first().full_name()),
            'owner_email': str(User.query.filter_by(id=card.user_id).first().email),
            'created': card.timestamp,
            'dh11_values': card.dht11_values.count(),
            'gaz_values': card.gaz_values.count(),
            '_links': {
                'self': '/api/cards/{}/'.format(card.id),
                'owner_url': '/api/users/{}/'.format(card.user_id),  # user_id
                # 'dht11_sensor': url_for('api.get_card_dht11', id=self.id)
            }
        }
        return jsonify(response)

    def delete(self, id):
        card = User.query.get_or_404(id)
        card.delete()
        db.session.commit()
        return jsonify({'Response': 'Success'})


class CardDht11API(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument('from_card_id', type=str, required=True)
    parse.add_argument('temperature', type=str)
    parse.add_argument('humidity', type=str)

    @staticmethod
    def get(id=None, page=1):  # GET

        card = Cards.query.get_or_404(id)
        response = {}
        for dht11 in card.dht11_values:
            response =  {
                'id_from_db': card.id,
                'owner_email': str(User.query.get_or_404(dht11.card_id).email),
                'from_card_id': dht11.card_id,
                'value_created_at': dht11.timestamp,
                'temperature': dht11.temperature,
                'humidity': dht11.humidity,
                '_links': {
                    'owner_url': '/api/users/{}'.format(User.query.get_or_404(dht11.card_id).id),
                    'card_url' : '/api/cards/{}'.format(dht11.card_id)

                }
            }
        return jsonify(response)

    def post(self, id):
        # create a new user
        args = self.parse.parse_args()
        temperature= args['temperature']
        humidity = args['humidity']
        from_card_id = args['from_card_id']
        card = Cards.query.get_or_404(id)
        if card is not None:
            dht11 = Dht11(temperature=temperature, humidity=humidity, card_id=from_card_id)
        db.session.add(dht11)
        db.session.commit()
        for dht11 in card.dht11_values:
            response = {
                'id_from_db': card.id,
                'owner_email': str(User.query.get_or_404(dht11.card_id).email),
                'from_card_id': dht11.card_id,
                'value_created_at': dht11.timestamp,
                'temperature': dht11.temperature,
                'humidity': dht11.humidity,
                '_links': {
                    'owner_url': '/api/users/{}'.format(User.query.get_or_404(dht11.card_id).id),
                    'card_url': '/api/cards/{}'.format(dht11.card_id)

            }
        }
        return jsonify(response)


API.add_resource(UserAPI, '/api/users/',  '/api/users/<int:id>/')
API.add_resource(CardsAPI, '/api/cards/', '/api/cards/<int:id>/', endpoint="card")
API.add_resource(UserCardAPI, '/api/users/<int:id_>/cards/')
API.add_resource(CardDht11API, '/api/cards/<int:id>/dht11/', endpoint="card_dht11")




""""
# api using flask_restless ?

from flask_restless import APIManager  # APIManger allow to creat RESTfull endpoints for SQLAlchemy model
from app import db, App
from app.models import User, Cards, Dht11, Gaz

api = APIManager(App, flask_sqlalchemy_db=db)
api.create_api(User, collection_name='users', methods=['GET', 'POST', 'PUT'])
api.create_api(Cards, collection_name='cards', methods=['GET', 'POST', 'PUT'])
api.create_api(Dht11, collection_name='dht11', methods=['GET', 'POST', 'PUT'])

"""""