from builtins import property

from app import db
from werkzeug.security import generate_password_hash  # to generate a hashed password
from werkzeug.security import check_password_hash      # to check the hashed password
from flask_login import UserMixin
from app import login
from datetime import datetime
from flask import url_for

class User(db.Model, UserMixin):
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
    def to_dict(self, include_email=False):
        data = {
            'id' : self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'last_seen': self.last_seen,  # isoformat() + 'Z',  ISO 8601 format, 'Z' timezone for UTC
            'about_me':self.about_me,
            'cards': self.cards.count(),
            '_links': {
                'self': url_for('api.get_user', id=self.id),
                'cards': url_for('api.get_cards', id=self.id),

            }

        }
        if include_email:
            data['email'] = self.email
        return data

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


class Cards(db.Model):
    __tablename__ = 'boards'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(48), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    dht11_value = db.relationship('Dht11', backref='dht11_sensor')
    gaz_value = db.relationship('Gaz', backref='gaz_sensor')

    def __repr__(self):
        return '{}'.format(self.name)


class Dht11(db.Model):
    __tablename__ = 'Dht11'
    id = db.Column(db.BigInteger, primary_key=True)
    temperature = db.Column(db.String(48), index=True)
    humidity = db.Column(db.String(48), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    card_id = db.Column(db.Integer, db.ForeignKey('boards.id'))

    def __repr__(self):
        return '<temp:{0}, humidity:{1}'.format(self.temperature, self.humidity)


class Gaz(db.Model):
    __tablename__ = 'Gaz'
    id = db.Column(db.BigInteger, primary_key=True)
    gaz = db.Column(db.String(48), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    card_id = db.Column(db.Integer, db.ForeignKey('boards.id'))

@login.user_loader
def load_user(id_):
    return User.query.get(int(id_))
