"""
@Filename: model.py(user)
@Project: *
@Author: lxliang912
@Date: 09/21/2018
@Description: create table user and insert data into table
"""
from passlib.apps import custom_app_context as pwd_context
from app.reference import db


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(128))

    # Stores a hash of password with the user
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    # Returns True if the password is correct or False if not
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)