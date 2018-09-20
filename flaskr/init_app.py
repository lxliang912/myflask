"""
@Filename: init_app.py
@Project: *
@Author: lxliang912
@Date: 9/18/2018
@Description: create flask app
"""
from . import task_view
from flask import Flask
from flask_cors import CORS
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

# sqlite
# DATABASE_PATH = 'sqlite:///database/todo.db'
# mysql
DATABASE_PATH = 'mysql+pymysql://root:admin@localhost:3310/lxliang-mysql'
api_name = '/todo/api/v1.0'

app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_PATH
# auto commit data into database while connection close
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)
# 配置允许跨域请求
CORS(app, supports_credentials=True)

api = Api(app)
api.add_resource(
    task_view.TaskListApi,
    api_name + '/tasks',
    api_name + '/tasks/',
    endpoint='tasks')
api.add_resource(
    task_view.TaskApi, api_name + '/tasks/<int:task_id>', endpoint='task')


class Task(db.Model):
    __tablename__ = 'task'

    task_id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(250), nullable=False)
    creation_date = db.Column(
        db.TIMESTAMP,
        server_default=db.func.current_timestamp(),
        nullable=False)
    done = db.Column(db.Boolean)

    def __init__(self, task_name, done):
        self.task_name = task_name
        self.done = done

    def __repr__(self):
        return '<task %r>' % self.task_name
