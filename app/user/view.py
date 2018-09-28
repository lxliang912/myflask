"""
@Filename: view.py(user)
@Project: *
@Author: lxliang912
@Date: 09/21/2018
@Description: Get data of user
"""
from flask import jsonify, request
from flask_restful import Resource

from app.utils.response import success, error
from app.reference import db
from .model import User


class RegisterApi(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if json_data['username'] is None:
            return error('username is null')
        elif json_data['password'] is None:
            return error('password is null')
        elif User.query.filter_by(
                username=json_data['username']).first() is not None:
            return error('user is already exist')
        else:
            user = User(username=json_data['username'])
            user.hash_password(json_data['password'])
            db.session.add(user)
            db.session.commit()
            return success('register success')
