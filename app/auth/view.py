"""
@Filename: view.py(user)
@Project: *
@Author: lxliang912
@Date: 09/21/2018
@Description: Get data of user
"""
from flask import jsonify, request, g
from flask_restful import Resource
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app.utils.util import request_return, request_code, is_empty
from app.reference import db
from .model import User, Token


class RegisterApi(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        username = json_data.get('username')
        password = json_data.get('password')

        # Username is empty
        if is_empty(username):
            return request_return('username is null', 'none')
        # Password is empty
        if is_empty(password):
            return request_return('password is null', 'none')
        # User is already exist
        elif User.query.filter_by(username=username).first() is not None:
            return request_return('user is already exist', 'exist')
        # Register new user
        else:
            user = User(username=username)
            user.hash_password(password)
            db.session.add(user)
            db.session.commit()
            return request_return('register success', 'success')


class LoginApi(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        username = json_data.get('username')
        password = json_data.get('password')

        # Username is empty
        if is_empty(username):
            return request_return('username is null', 'none')
        # Password is empty
        if is_empty(password):
            return request_return('password is null', 'none')
        # Post data format is right
        else:
            user = User.query.filter_by(username=username).first()
            # User is exist
            if user is not None:
                # Argument must be hash password
                user_password = User(password_hash=user.password_hash)
                # Check login password
                if not user_password.verify_password(password):
                    return request_return('wrong password', 'none')
                # Login success, return token auth
                else:
                    return request_return(
                        {
                            'status': 'login success',
                            'data': Token(user.username).generate_auth_token()
                        }, 'success')
            # User is not exist in the database
            else:
                return request_return(
                    'user is not exist, please register first', 'none')
