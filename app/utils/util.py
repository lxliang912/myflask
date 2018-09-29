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


def request_return(message, code_name):
    return jsonify({
        'code': request_code[code_name],
        'data': {
            'message': message
        }
    })


def is_empty(data):
    if data is None or data == '':
        return True
    else:
        return False
