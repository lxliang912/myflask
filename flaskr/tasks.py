from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for, jsonify)
from flaskr.db import get_db
import json

# 创建一个tasks蓝图
bp = Blueprint('tasks', __name__)


# 获取任务列表
@bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = get_db().execute('SELECT * FROM task').fetchall()
    task_list = []

    for i in tasks:
        task_list.append(json_data(i))

    # return jsonify({'code': 2000, 'data': {tasks: task_list}})
    return jsonify(task_list)


# 获取指定任务
@bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = get_db().execute('SELECT * FROM task WHERE id = ?',
                            (task_id, )).fetchone()
    # 检查查询的任务十分存在
    if task is None:
        return jsonify({
            'code': 403,
            'data': {
                'message': "task id {0} doesn't exist.".format(task_id)
            }
        })
    # 任务存在返回数据
    else:
        return jsonify(json_data(task))
        # return json.dumps({'code': 2000, 'data': {'task': task}})


def json_data(sql_data):
    return {
        'id': sql_data[0],
        'title': sql_data[1],
    }


# 创建一个任务
@bp.route('/tasks/create', methods=('GET', 'POST'))
def create_task():
    if request.method == 'POST':
        data = request.json
        title = data['title']
        error = None

        if title is None:
            return 'title is require'

        task = get_db().execute('SELECT * FROM task WHERE title = ?',
                                (title, )).fetchone()

        # 创建前判断任务是否已存在
        if task is not None:
            error = 'task [{}] is already exist.'.format(title)
            return jsonify({'code': 403, 'data': {'message': error}})

        # 创建任务
        elif task is None:
            get_db().execute(
                'INSERT INTO task (title, is_done)'
                ' VALUES (?, ?)', (title, False))
            get_db().commit()
            return jsonify({
                'code': 2000,
                'data': {
                    'message': 'create success'
                }
            })
