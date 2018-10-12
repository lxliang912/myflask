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
        result_data = check_token(token, TaskListApi.get_task_list, '')
        return request_return(result_data['data'], result_data['code'])

    @staticmethod
    def get_task_list(data):
        task_list = []
        tasks = Task.query.all()

        if len(tasks) < 1:
            return request_return('not task', 'success')
        elif len(tasks) > 0:
            for i in tasks:
                task_list.append({
                    'task_id': i.task_id,
                    'task_name': i.task_name,
                    'done': i.done,
                })
            return {'data': task_list, 'code': 'success'}

    """
    Create only one task each time
    # argument: task_name(string), done(boolean)
    # both necessary
    """

    def post(self):
        token = request.headers.get('token')
        result_data = check_token(token, TaskListApi.new_task, '')
        return request_return(result_data['data'], result_data['code'])

    @staticmethod
    def new_task(data):
        json_data = request.get_json(force=True)
        task_name = json_data['task_name']
        task_status = json_data['done']

        if is_empty(task_name):
            return {'data': 'task name is necessary', 'code': 'none'}
        elif is_empty(task_status):
            return {'data': 'task status is necessary', 'code': 'none'}
        elif Task.query.filter_by(task_name=task_name).first() is not None:
            return {'data': 'task is already exist', 'code': 'exist'}
        else:
            db.session.add(Task(task_name, task_status))
            db.session.commit()
            return {'data': 'create success', 'code': 'success'}


class TaskApi(Resource):
    # Get data of task by task id
    def get(self, task_id):
        token = request.headers.get('token')
        result_data = check_token(token, TaskApi.get_task, task_id)
        return request_return(result_data['data'], result_data['code'])

    @staticmethod
    def get_task(task_id):
        task = Task.query.filter(Task.task_id == task_id).first()

        if task is None:
            return {'data': 'task is not exist', 'code': 'none'}
        else:
            return {
                'data': {
                    'task_id': task_id,
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
        result_data = check_token(token, TaskApi.update_task, task_id)
        return request_return(result_data['data'], result_data['code'])

    @staticmethod
    def update_task(task_id):
        json_data = request.get_json(force=True)
        task_name = json_data['task_name']
        task_status = json_data['done']
        task = Task.query.filter(Task.task_id == task_id).first()

        if task is None:
            return {'data': 'task is not exist', 'code': 'exist'}
        else:
            task.task_name = task_name
            task.done = task_status
            db.session.commit()
            return {'data': 'modify success', 'code': 'success'}

    # Delete task by task id
    def delete(self, task_id):
        token = request.headers.get('token')
        result_data = check_token(token, TaskApi.delete_task, task_id)
        return request_return(result_data['data'], result_data['code'])

    @staticmethod
    def delete_task(task_id):
        task = Task.query.filter(Task.task_id == task_id).first()

        if task is None:
            return {'data': 'task is not exist', 'code': 'exist'}
        else:
            db.session.delete(task)
            db.session.commit()
            return {'data': 'delete success', 'code': 'success'}
