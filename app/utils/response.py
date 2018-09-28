"""
@FileName: response.py
@Project: *
@Author: lxliang912
@Date: 9/18/2018
@Description: return json data of users request
"""
from flask import jsonify

request_code = {
    'success': 200,
    'none': 401,
    'net_error': 500,
    'error': 404,
    'exist': 201,
}


def return_code(message, code_name):
    return jsonify({
        'code':code_name,
        'data': {
            'message': message
        }
    })
