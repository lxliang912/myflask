"""
@Filename: model.py(user)
@Project: *
@Author: lxliang912
@Date: 09/21/2018
@Description: create table user and insert data into table
"""
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)
from flask import current_app, g
from flask_httpauth import HTTPBasicAuth

from app.reference import db

auth = HTTPBasicAuth()


class Auth(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), index=True)
    password_hash = db.Column(db.String(256))

    # When register success, stores a hash of password with the user
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    @auth.verify_password
    def verify_password(self, password):
        # First try to authenticate by token
        user = Auth.verify_auth_token(username_or_token)
        # Try to authenticate with username/password
        if not user:
            user = Auth.query.filter_by(username=username_or_token).first()
            if not user or not user.verify_password(password):
                return False
        g.user = user
        return True

    # Genrate token when login success
    def generate_auth_token(self, expiration=7200):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = Auth.query.get(data['username']).first()
        return user