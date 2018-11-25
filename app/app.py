"""
@Filename: app.py
@Project: *
@Author: lxliang912
@Date: 9/18/2018
@Description: Create flask app and initialized reference with app
"""
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from .config import DATABASE_PATH
from .reference import db, api
# import routers
from . import router


# Create a flask app factory
def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Use to connect database
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_PATH
    # Auto commit data into database while connection close
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    # Track the modified of object and send signal, need more memory
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # create database table

    # Access-Control-Allow-Origin
    CORS(app, supports_credentials=True)

    init_reference(app)

    return app


# Each reference is initialized in the app factory
def init_reference(app):
    db.init_app(app)
    api.init_app(app)


db.create_all(app=create_app())