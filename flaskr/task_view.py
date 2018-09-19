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
    def get(self):
        task_list = []
        tasks = init_app.Task.query.all()

        if len(tasks) < 1:
            return returnJsonData(2000, 'not task')
        elif len(tasks) > 0:
            for i in tasks:
                task_list.append({
                    'id': i.id,
                    'task_name': i.task_name,
                    'done': i.done,
                })
            return success(task_list)

    def post(self):
        json_data = request.get_json(force=True)
        if json_data['task_name'] is None:
            return error('task name is necessary')
        elif json_data['done'] is None:
            return error('conform task status')
        else:
            task = {
                'task_name': json_data['task_name'],
                'done': json_data['done']
            }

            init_app.db.session.add_all(task)
            init_app.db.session.commit()
            return success('create success')