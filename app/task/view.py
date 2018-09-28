"""
@Filename: tasks.py
@Project: *
@Author: lxliang912
@Date: 9/18/2018
@Description: Get data of task
"""
from flask import jsonify, request
from flask_restful import Resource

from app.utils.response import return_code, request_code
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
            return return_code('not task', request_code['success'])
        elif len(tasks) > 0:
            for i in tasks:
                task_list.append({
                    'task_id': i.task_id,
                    'task_name': i.task_name,
                    'done': i.done,
                })
            return return_code(task_list, request_code['success'])

    """
    Create only one task each time
    # argument: task_name(string), done(boolean)
    # both necessary
    """

    def post(self):
        json_data = request.get_json(force=True)
        if json_data['task_name'] is None:
            return return_code('task name is necessary', request_code['none'])
        elif json_data['done'] is None:
            return return_code('task status is necessary', request_code['none'])
        elif Task.query.filter_by(task_name=task_name).first() is not None:
            return return_code('task is already exist', request_code['exist'])
        else:
            db.session.add(Task(json_data['task_name'], json_data['done']))
            db.session.commit()
            return return_code('create success', request_code['success'])


class TaskApi(Resource):
    # Get data of task by task id
    def get(self, task_id):
        task = Task.query.filter(Task.task_id == task_id).first()
        if task is None:
            return return_code('task is not exist', request_code['none'])
        else:
            return return_code({
                'task_id': task_id,
                'task_name': task.task_name,
                'creation_date': task.creation_date,
                'done': task.done
            }, request_code['success'])

    """
    Modify data of task by task id
    # argument: task_name(string), done(boolean)
    """

    def put(self, task_id):
        json_data = request.get_json(force=True)
        task = Task.query.filter(Task.task_id == task_id).first()

        if task is None:
            return return_code('task is not exist', request_code['exist'])
        else:
            task.task_name = json_data['task_name']
            task.done = json_data['done']
            db.session.commit()
            return return_code('modify success', request_code['success'])

    # Delete task by task id
    def delete(self, task_id):
        task = Task.query.filter(Task.task_id == task_id).first()

        if task is None:
            return return_code('task is not exist', request_code['exist'])
        else:
            db.session.delete(task)
            db.session.commit()
            return return_code('delete success', request_code['success'])
