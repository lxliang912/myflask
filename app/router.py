"""
@Filename: router.py
@Project: *
@Author: lxliang912
@Date: 09/21/2018
@Description: interface url
"""
from flask_restful import Resource

from app.reference import api
from app.config import api_name

# Import task router
from app.task.view import TaskApi, TaskListApi

# Router list
api.add_resource(
    TaskListApi, api_name + '/tasks', api_name + '/tasks/', endpoint='tasks')
api.add_resource(TaskApi, api_name + '/tasks/<int:task_id>', endpoint='task')
