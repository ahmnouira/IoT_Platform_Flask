from app import db
from werkzeug.security import  generate_password_hash  # to generate a hashed password
from werkzeug.security import check_password_hash      # to check the hashed password
from flask_login import UserMixin
from app import login
from datetime import datetime


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64), index=True)
    lastname = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(32))
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    cards = db.relationship('Card', backref='owner', lazy='dynamic')

    def __repr__(self):
        return '<User {0} {1}>'.format(self.firstname, self.lastname)

    def set_password(self, password):  # hashing method
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):  # validate password method
        return check_password_hash(self.password_hash, password)


class Role(db.Model):
    __tablename__ ='roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64)) #!!!!!!!!! unique
    # each role can belong to many users, but one user can have one role
    users = db.relationship('User', backref='role')


    def __repr__(self):
        return '<Role {}>'.format(self.name)


class Card(db.Model):
    __tablename__ = 'boards'
    id = db.Column(db.Integer, primary_key=True)
    type_ = db.Column(db.String(48), index=True)
    # e
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Card {}>'.format(self.type_)


class Dht11(db.Model):
    __tablename__ = 'dht11'
    id = db.Column(db.BigInteger, primary_key=True)
    temperature = db.Column(db.String(48), index=True)
    humidity = db.Column(db.String(48), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


class Gaz(db.Model):
    __tablename__ = 'gaz'
    id = db.Column(db.BigInteger, primary_key=True)
    gaz = db.Column(db.String(48), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
