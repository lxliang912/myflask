from flask_restful import Resource
from . import init_app
from flask import jsonify


class Todo(Resource):
    def get(self):
        tasks = init_app.Task.query.all()
        return jsonify(list(tasks))
