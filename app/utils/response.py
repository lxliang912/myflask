"""
@FileName: response.py
@Project: *
@Author: lxliang912
@Date: 9/18/2018
@Description: return json data of users request
"""
from flask import jsonify


def success(data):
    return jsonify({'code': 2000, 'data': data})


def error(message):
    return jsonify({'code': 2010, 'data': {'message': message}})
