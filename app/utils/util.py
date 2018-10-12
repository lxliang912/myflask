"""
@FileName: response.py
@Project: *
@Author: lxliang912
@Date: 9/18/2018
@Description: return json data of users request
"""
from flask import jsonify

from app.auth.model import Token

# request code
request_code = {
    'success': 200,
    'none': 401,
    'net_error': 500,
    'error': 404,
    'exist': 201,
}


# return request data
def request_return(message, code_name):
    return jsonify({
        'code': request_code[code_name],
        'data': {
            'message': message
        }
    })


# check data is empty
def is_empty(data):
    if data is None or data == '':
        return True
    else:
        return False


# Token argument is not exist
def check_token(token, callback, argument):
    if is_empty(token):
        return {'data': 'please login first', 'code': 'error'}
    # Token is wrong
    elif Token.verify_auth_token(token) is None:
        return {'data': 'token is wrong', 'code': 'error'}
    # Token verify success
    elif not Token.verify_auth_token(token):
        return callback(argument)