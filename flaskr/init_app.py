from . import tasks
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
    id = db.Column(db.Integer, primary_key=True)
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


@app.before_first_request
def init_database():
    db.drop_all()
    db.create_all()
    tasks = {Task('test task', False)}
    db.session.add_all(tasks)
    db.session.commit()


api = Api(app)
api.add_resource(tasks.Todo, '/')