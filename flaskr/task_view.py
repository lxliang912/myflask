"""
@Filename: tasks.py
@Project: *
@Author: lxliang912
@Date: 9/18/2018
@Description: Get data of task
"""
from . import init_app
from flask import jsonify, request
from flask_restful import Resource
from flaskr.utils.response import success, error


class TaskApi(Resource):
    # get method, get all task data
    def get(self):
        task_list = []
        tasks = init_app.Task.query.all()

        if len(tasks) < 1:
            return success('not task')
        elif len(tasks) > 0:
            for i in tasks:
                task_list.append({
                    'task_id': i.task_id,
                    'task_name': i.task_name,
                    'done': i.done,
                })
            return success(task_list)

    # post method, create only one task each time
    def post(self):
        json_data = request.get_json(force=True)
        if json_data['task_name'] is None:
            return error('task name is necessary')
        elif json_data['done'] is None:
            return error('task status is necessary')
        elif check_task_exist(json_data['task_name']):
            return error('task is already exist')
        else:
            init_app.db.session.add(
                init_app.Task(json_data['task_name'], json_data['done']))
            init_app.db.session.commit()
            return success('create success')

    # put method, modify task data by task id
    def put(self):
        json_data = request.get_json(force=True)
        task = init_app.Task.query.filter(
            init_app.Task.task_id == json_data['task_id']).first()

        if task is None:
            return error('task is not exist')
        else:
            task.task_name = json_data['task_name']
            task.done = json_data['done']
            init_app.db.session.commit()
            return success('modify success')

    def delete(self):
        json_data = request.get_json(force=True)
        task = init_app.Task.query.filter(
            init_app.Task.task_id == json_data['task_id']).first()

        if task is None:
            return error('task is not exist')
        else:
            init_app.db.session.delete(task)
            init_app.db.session.commit()
            return success('delete success')


def check_task_exist(task_name):
    task = init_app.Task.query.filter(
        init_app.Task.task_name == task_name).first()
    if task is not None:
        return True
    else:
        return False