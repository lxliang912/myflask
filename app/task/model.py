"""
@Filename: model.py(task)
@Project: *
@Author: lxliang912
@Date: 09/21/2018
@Description: create table task and insert data into table
"""
from app.reference import db


class Task(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(250), nullable=False)
    creation_date = db.Column(
        db.TIMESTAMP,
        server_default=db.func.current_timestamp(),
        nullable=False)
    done = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('user', lazy='dynamic'))

    def __init__(self, task_name, done, user):
        self.task_name = task_name
        self.done = done
        self.user = user
