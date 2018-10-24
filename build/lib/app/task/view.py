"""
@Filename: tasks.py
@Project: *
@Author: lxliang912
@Date: 9/18/2018
@Description: Get data of task
"""
from flask import jsonify, request
from flask_restful import Resource

from app.utils.util import request_return, is_empty, check_token
from app.reference import db
from .model import Task
from ..auth.model import Token


class TaskListApi(Resource):
    """
    Get task list
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
        }, TaskListApi.get_task_list)

        return request_return(result_data['data'], result_data['code'])

    @staticmethod
    def get_task_list(data):
        task_list = []
        # get task list by paginate, return data by ascending or descending (default Ascending)
        # method: asc , desc
        tasks_data = Task.query.order_by(Task.task_id.asc()).paginate(
            data['page'], per_page=data['per_page'], error_out=False)

        if len(tasks_data.items) < 1:
            return {'data': {'message': 'not task'}, 'code': 'success'}
        elif len(tasks_data.items) > 0:
            for task in tasks_data.items:
                task_list.append({
                    'task_id': task.task_id,
                    'task_name': task.task_name,
                    'done': task.done,
                })
            return {
                'data': {
                    'message': 'success',
                    'task_list': task_list,
                    'pages': tasks_data.pages,
                    'cur_page': tasks_data.page,
                    'per_page': tasks_data.per_page,
                    'total': tasks_data.total
                },
                'code': 'success'
            }

    """
    Create only one task each time
    # argument: task_name(string), done(boolean)
    # both necessary
    """

    def post(self):
        token = request.headers.get('token')
        result_data = check_token({
            'token': token,
            'data': {}
        }, TaskListApi.new_task)

        return request_return(result_data['data'], result_data['code'])

    @staticmethod
    def new_task(data):
        json_data = request.get_json(force=True)
        task_name = json_data['task_name']
        task_status = json_data['done']

        if is_empty(task_name):
            return {
                'data': {
                    'message': 'task name is necessary'
                },
                'code': 'none'
            }
        elif is_empty(task_status):
            return {
                'data': {
                    'message': 'task status is necessary'
                },
                'code': 'none'
            }
        elif Task.query.filter_by(task_name=task_name).first() is not None:
            return {
                'data': {
                    'message': 'task is already exist'
                },
                'code': 'exist'
            }
        else:
            db.session.add(Task(task_name, task_status))
            db.session.commit()
            return {'data': {'message': 'create success'}, 'code': 'success'}


class TaskApi(Resource):
    # Get data of task by task id
    def get(self, task_id):
        token = request.headers.get('token')
        result_data = check_token({
            'token': token,
            'data': {
                'task_id': task_id
            }
        }, TaskApi.get_task)
        return request_return(result_data['data'], result_data['code'])

    @staticmethod
    def get_task(data):
        task = Task.query.filter(Task.task_id == data['task_id']).first()

        if task is None:
            return {'data': 'task is not exist', 'code': 'none'}
        else:
            return {
                'data': {
                    'task_id': data['task_id'],
                    'task_name': task.task_name,
                    'creation_date': task.creation_date,
                    'done': task.done
                },
                'code': 'success'
            }

    """
    Modify data of task by task id
    # argument: task_name(string), done(boolean)
    """

    def put(self, task_id):
        token = request.headers.get('token')
        result_data = check_token({
            'token': token,
            'data': {
                'task_id': task_id
            }
        }, TaskApi.update_task)

        return request_return(result_data['data'], result_data['code'])

    @staticmethod
    def update_task(data):
        json_data = request.get_json(force=True)
        task_name = json_data['task_name']
        task_status = json_data['done']
        task = Task.query.filter(Task.task_id == data['task_id']).first()

        if task is None:
            return {'data': {'message': 'task is not exist'}, 'code': 'exist'}
        else:
            task.task_name = task_name
            task.done = task_status
            db.session.commit()
            return {'data': {'message': 'modify success'}, 'code': 'success'}

    # Delete task by task id
    def delete(self, task_id):
        token = request.headers.get('token')
        result_data = check_token({
            'token': token,
            'data': {
                'task_id': task_id
            }
        }, TaskApi.delete_task)

        return request_return(result_data['data'], result_data['code'])

    @staticmethod
    def delete_task(data):
        task = Task.query.filter(Task.task_id == data['task_id']).first()

        if task is None:
            return {'data': {'message': 'task is not exist'}, 'code': 'exist'}
        else:
            db.session.delete(task)
            db.session.commit()
            return {'data': {'message': 'delete success'}, 'code': 'success'}
