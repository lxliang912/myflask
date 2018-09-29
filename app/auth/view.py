"""
@Filename: view.py(user)
@Project: *
@Author: lxliang912
@Date: 09/21/2018
@Description: Get data of user
"""
from flask import jsonify, request, g
from flask_restful import Resource

from app.utils.util import request_return, request_code, is_empty
from app.reference import db
from .model import Auth


class RegisterApi(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        username = json_data['username']
        password = json_data['password']

        # Username is empty
        if is_empty(username):
            return request_return('username is null', 'none')
        # Password is empty
        if is_empty(password):
            return request_return('password is null', 'none')
        # User is already exist
        elif Auth.query.filter_by(username=username).first() is not None:
            return request_return('user is already exist', 'exist')
        # Register new user
        else:
            user = Auth(username=username)
            user.hash_password(password)
            db.session.add(user)
            db.session.commit()
            return request_return('register success', 'success')


class LoginApi(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        username = json_data['username']
        password = json_data['password']

        # Username is empty
        if is_empty(username):
            return request_return('username is null', 'none')
        # Password is empty
        if is_empty(password):
            return request_return('password is null', 'none')
        else:
            # Login success
            if Auth.query.filter_by(username=username).first() is not None:
                token = Auth.generate_auth_token(7200)
                return request_return(token, 'success')
            # User is not exist in the database
            else:
                return request_return(
                    'user is not exist, please register first', 'none')
