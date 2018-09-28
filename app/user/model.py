"""
@Filename: model.py(user)
@Project: *
@Author: lxliang912
@Date: 09/21/2018
@Description: create table user and insert data into table
"""
from app.reference import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password = db.Column(db.String(128))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return 'username %r' % self.username