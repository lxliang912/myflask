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

DATABASE_PATH = 'database/todo.db'

app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
# 配置允许跨域请求
CORS(app, supports_credentials=True)


class Task(db.Model):
    # __tablename__ = 'task'
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


# 初始化数据库时先清除数据，再重新创建
@app.before_first_request
def init_database():
    db.drop_all()
    db.create_all()


api = Api(app)
api.add_resource(task_view.TaskApi, '/todo')