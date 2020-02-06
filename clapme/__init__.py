from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from views.viewss import ApiUserGoalList, ApiUserGoal

app = Flask(__name__)
app.config.from_object('config')

api = Api(app)
db = SQLAlchemy(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')
api.add_resource(ApiUserGoalList, '/user-goal/')
api.add_resource(ApiUserGoal, '/user-goal/<int:goal_id>')


if __name__ == '__main__':
    app.run(debug=True)
