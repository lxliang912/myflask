"""
@Filename: view.py(user)
@Project: *
@Author: lxliang912
@Date: 11/28/2018
@Description: Get data of user
"""
from flask import request
from flask_restful import Resource

from app.utils.util import request_return, is_empty, check_token, get_userinfo
from app.reference import db
from app.auth.model import Token, User


class UserListApi(Resource):
    """
    Only administrator can get all user list 
    """

    def get(self):
        token = request.headers.get('token')
        # if per_page is None, set default value 1
        page = request.args.get('page', 1, type=int)
        # if per_page is None, set default value 10
        per_page = request.args.get('per_page', 10, type=int)

        result_data = check_token({
            'token': token,
            'data': {
                'page': page,
                'per_page': per_page
            }
        }, self.get_user_list)

        return request_return(result_data['data'], result_data['code'])

    @classmethod
    # Return user list with json type
    def return_users(cls, user_list):
        def to_json(user):
            return {
                'id': user.id,
                'user_name': user.username,
            }

        return list(map(lambda user: to_json(user), user_list))

    @classmethod
    def get_user_list(cls, data, token):
        user_list = []
        user_data = User.query.order_by(User.id.asc()).paginate(
            page=data['page'], per_page=data['per_page'], error_out=False)

        if len(user_data.items) < 1:
            return {'data': {'message': 'not users'}, 'code': 'success'}
        elif len(user_data.items) > 0:
            return {
                'data': {
                    'message': 'success',
                    'user_list': cls.return_users(user_data.items),
                    'pages': user_data.pages,
                    'cur_page': user_data.page,
                    'per_page': user_data.per_page,
                    'total': user_data.total
                },
                'code': 'success'
            }