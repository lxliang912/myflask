"""
@FileName: response.py
@Project: *
@Author: lxliang912
@Date: 9/18/2018
@Description: Util function
"""
from flask import jsonify

from app.auth.model import Token

# Request code
request_code = {
    'success': 200,
    'none': 401,
    'net_error': 500,
    'error': 404,
    'exist': 201,
}


# Return request data
def request_return(data, code_name):
    return jsonify({'code': request_code[code_name], 'data': data})


# Check data is empty
def is_empty(data):
    if data is None or data == '':
        return True
    else:
        return False


# Check token while auth request
def check_token(arguments, callback):
    if is_empty(arguments['token']):
        return {'data': 'please login first', 'code': 'error'}
    # Token is expired
    elif Token.verify_auth_token(arguments['token']) == 'expired':
        return {'data': 'token is expired, please login again', 'code': 'none'}
    # Token is invalid
    elif Token.verify_auth_token(arguments['token']) == 'invalid':
        return {'data': 'token is invalid', 'code': 'error'}
    # Token verify success
    elif not Token.verify_auth_token(arguments['token']):
        return callback(arguments['data'])