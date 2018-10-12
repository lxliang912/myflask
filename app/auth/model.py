"""
@Filename: model.py(user)
@Project: *
@Author: lxliang912
@Date: 09/21/2018
@Description: create table user and insert data into table
"""
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)
from flask import current_app
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash, generate_password_hash

from app.reference import db
import app.utils.util as util


class Auth(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), index=True)
    password_hash = db.Column(db.String(256))

    # When register success, stores password with hash of the user
    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Check password
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Token(object):
    def __init__(self, username):
        self.username = username

    # Generate token if login success
    def generate_auth_token(self, expiration=3600):
        s = Serializer('SECRET_KEY', expiration)
        return {
            'token': s.dumps({
                'username': self.username
            }).decode('ascii'),
            'expired': expiration
        }

    # verify token
    def verify_auth_token(token):
        s = Serializer('SECRET_KEY')
        try:
            data = s.loads(token)
            return util.is_empty(
                Auth.query.filter(Auth.username == data['username']).first())
        # Valid token, but expired
        except SignatureExpired:
            return 'expired'
        # Invalid token
        except BadSignature:
            return 'invalid'