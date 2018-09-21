"""
@Filename: database.py
@Project: *
@Author: lxliang912
@Date: 09/21/2018
@Description: init reference located in app.py
"""
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

db = SQLAlchemy()
api = Api()
