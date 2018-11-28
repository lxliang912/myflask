"""
@Filename: router.py
@Project: *
@Author: lxliang912
@Date: 09/21/2018
@Description: Api router list
"""
from app.reference import api
from app.config import api_name

# Api class
from app.task.view import TaskApi, TaskListApi
from app.auth.view import RegisterApi, LoginApi
from app.user.view import UserListApi

# Router list
api.add_resource(
    TaskListApi, api_name + '/tasks', api_name + '/tasks/', endpoint='tasks')
api.add_resource(TaskApi, api_name + '/task/<int:id>', endpoint='task')
api.add_resource(RegisterApi, api_name + '/register', endpoint='register')
api.add_resource(LoginApi, api_name + '/login', endpoint='login')
api.add_resource(UserListApi, api_name + '/users', endpoint='users')