from builtins import property

from app import db
from werkzeug.security import generate_password_hash  # to generate a hashed password
from werkzeug.security import check_password_hash      # to check the hashed password
from flask_login import UserMixin
from app import login
from datetime import datetime
from flask import url_for, jsonify


# Paginated representation mixi, class
class PaginatedAPIMxin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
           '_links': {
                'self': endpoint,
               'next': url_for(endpoint, page=page + 1, per_page=per_page, **kwargs) if resources.has_next
                else None,
               'perv': url_for(endpoint, page=page - 1, per_page=per_page, **kwargs) if resources.has_prev
                else None

            }
        }
        return data


class User(PaginatedAPIMxin, db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64), index=True)
    lastname = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(32))
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    created_timestamp = db.Column(db.DateTime, default=datetime.now)
    about_me = db.Column(db.String(140))  # about_me
    admin = db.Column(db.Boolean, default=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    cards = db.relationship('Cards', backref='owner', lazy='dynamic')

    def __repr__(self):
        return '{0} {1}, {2}'.format(self.firstname, self.lastname, self.email)

    def set_password(self, password):  # hashing method
        self.password_hash = generate_password_hash(password)

    def is_admin(self):
        return self.admin

    # converts a user object to python representation need it for API
    # serialization
    def to_dict(self, include_email=False):
        data = {
            'id' : self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'last_seen': self.last_seen,  # isoformat() + 'Z',  ISO 8601 format, 'Z' timezone for UTC
            'about_me': self.about_me,
            'cards': self.cards.count(),
            '_links': {
                'self': url_for('api.get_user', id=self.id),
                'your_cards': url_for('api.get_user_cards', id=self.id),

            }

        }
        if include_email:
            data['email'] = self.email
        return data

    # deserialization JSON back to a model
    def form_dict(self, data, new_user=False):
        for field in data:
            setattr(self, field, data)  # set the new value of attribute
        if new_user and 'password' in data:
            self.set_password(data['password'])

    @staticmethod
    def make_password(password):
        return generate_password_hash(password)

    def check_password(self, password):  # validate password method
        return check_password_hash(self.password_hash, password)

    @property
    def user_password(self):
        return str(self.password_hash)[20:40]

    @property                         # property to return value of about_me
    def about_me_(self):
        return str(self.about_me)[:100]

    def full_name(self):
        return str(self.firstname) + " " + str(self.lastname)
   # @property
   # def cards(self):
    #    return ','.join(card.type_ for card in self.cards )


class Role(db.Model):
    __tablename__ ='roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64)) #!!!!!!!!! unique
    # each role can belong to many users, but one user can have one role
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '{}'.format(self.name)


class Cards(PaginatedAPIMxin, db.Model):
    __tablename__ = 'boards'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(48), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    dht11_values = db.relationship('Dht11', backref='form_card_', lazy='dynamic')
    gaz_values = db.relationship('Gaz', backref='from_card', lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.name)

    # serialization: to JSON
    def to_dict(self):
        data = {
            'id': self.id,
            'owner_name': str(Cards.query.get_or_404(self.id).owner.full_name()),
            'owner_email': str(Cards.query.get_or_404(self.id).owner.email),
            'card_name': self.name,
            'created': self.timestamp,
            'dh11_values': self.dht11_values.count(),
            'gaz_values': self.gaz_values.count(),
           # '_links': {
            #    'self': url_for('api.get_card', id=self.id),
             #   'owner_url': url_for('api.get_user', id=self.user_id),  # user_id
              #  'dht11_sensor': url_for('api.get_card_dht11', id=self.id)

               # }

            }


        return data


    # desialization from JSON --> to model
    @staticmethod
    def from_json(card_post):
        name = card_post.get('name')   # check forms for regsiter a card
        if name is None or name =='':
            raise ValidationError('Card does not have a name')

        return Cards(name=name)

class Dht11(PaginatedAPIMxin, db.Model):
    __tablename__ = 'Dht11'
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.String(48), index=True)
    humidity = db.Column(db.String(48), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    card_id = db.Column(db.Integer, db.ForeignKey('boards.id'))

    def __repr__(self):
        return '<temp:{0}, humidity:{1}'.format(self.temperature, self.humidity)

    def to_dict(self):
        data = {
            'id_from_db': self.id,
            'owner_email': str(User.query.get_or_404(self.card_id).email),
            'from_card_id': self.card_id,
            'value_created_at': self.timestamp,
            'temperature': self.temperature,
            'humidity': self.humidity,
            '_links': {
              #  'self': url_for('api.get_card_dht11', id= self.card_id),
               # 'owner_url': url_for('api.get_user', id= User.query.get_or_404(self.card_id).id) # user_id

                }

            }

        return data




class Gaz(PaginatedAPIMxin, db.Model):
    __tablename__ = 'Gaz'
    id = db.Column(db.BigInteger, primary_key=True)
    gaz = db.Column(db.String(48), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    card_id = db.Column(db.Integer, db.ForeignKey('boards.id'))


@login.user_loader
def load_user(id_):
    return User.query.get(int(id_))
