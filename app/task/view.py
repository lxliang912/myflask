"""
@Filename: tasks.py
@Project: *
@Author: lxliang912
@Date: 9/18/2018
@Description: Get data of task
"""
from flask import jsonify, request
from flask_restful import Resource

from app.utils.util import request_return, is_empty
from app.reference import db
from .model import Task


class TaskListApi(Resource):
    """
    Get task list
    """

    def get(self):
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
            return request_return(task_list, 'success')

    """
    Create only one task each time
    # argument: task_name(string), done(boolean)
    # both necessary
    """

    def post(self):
        json_data = request.get_json(force=True)
        task_name = json_data['task_name']
        task_status = json_data['done']

        if is_empty(task_name):
            return request_return('task name is necessary', 'none')
        elif is_empty(task_status):
            return request_return('task status is necessary', 'none')
        elif Task.query.filter_by(task_name=task_name).first() is not None:
            return request_return('task is already exist', 'exist')
        else:
            db.session.add(Task(task_name, task_status))
            db.session.commit()
            return request_return('create success', 'success')


class TaskApi(Resource):
    # Get data of task by task id
    def get(self, task_id):
        task = Task.query.filter(Task.task_id == task_id).first()
        if task is None:
            return request_return('task is not exist', 'none')
        else:
            return request_return({
                'task_id': task_id,
                'task_name': task.task_name,
                'creation_date': task.creation_date,
                'done': task.done
            }, 'success')

    """
    Modify data of task by task id
    # argument: task_name(string), done(boolean)
    """

    def put(self, task_id):
        json_data = request.get_json(force=True)
        task_name = json_data['task_name']
        task_status = json_data['done']
        task = Task.query.filter(Task.task_id == task_id).first()

        if task is None:
            return request_return('task is not exist', 'exist')
        else:
            task.task_name = task_name
            task.done = task_status
            db.session.commit()
            return request_return('modify success', 'success')

    # Delete task by task id
    def delete(self, task_id):
        task = Task.query.filter(Task.task_id == task_id).first()

        if task is None:
            return request_return('task is not exist', 'exist')
        else:
            db.session.delete(task)
            db.session.commit()
            return request_return('delete success', 'success')
