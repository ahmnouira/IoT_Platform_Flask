from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    def __repr__(self):
        return '<User {}>'.format(self.username)


class Dht11(db.Model):
    __tablename__ = 'dht11'
    id = db.Column(db.BigInteger, primary_key=True)
    temperature = db.Column(db.SmallInteger, index=True)
    humidity = db.Column(db.SmallInteger, index=True)
    record = db.Column(db.DateTime, index=True, nullable=False)


class Gaz(db.Model):
    __tablename__ = 'gaz'
    id = db.Column(db.BigInteger, primary_key=True)
    values = db.Column(db.String(48), index=True)