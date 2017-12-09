# project/server/models.py


import datetime

from passlib.hash import pbkdf2_sha512

from project.server import db


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    _password = db.Column('password', db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, *args, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = pbkdf2_sha512.hash(password)

    def is_password_valid(self, password):
        return pbkdf2_sha512.verify(password, self.password)

    def __repr__(self):
        return '<User {0}>'.format(self.email)
