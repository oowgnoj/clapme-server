from flask_restful import Resource

from .auth import ApiLogin
from .views import ApiUserGoal, ApiGoalSuccess, ApiGoalCommentList, ApiGoalComment, ApiUser, ApiGoal, ApiHistory, ApiReaction, ApiUserReaction


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


def initialize_routes(api):
    api.add_resource(HelloWorld, '/')
    api.add_resource(ApiLogin, '/login/')
    api.add_resource(ApiGoal, '/goal/', '/goal/<int:id>')
    api.add_resource(ApiUserGoal, '/user-goal/', '/user-goal/<int:goal_id>')
    api.add_resource(ApiGoalSuccess, '/goal-success/',
                     '/goal-success/<int:goal_id>')
    api.add_resource(ApiGoalCommentList, '/goal-comment/<int:goal_id>')
    api.add_resource(ApiGoalComment, '/goal-comment/',
                     '/goal-comment/<int:comment_id>')
    api.add_resource(ApiUser, '/user/')
    api.add_resource(ApiHistory, '/history/<int:id>')
    api.add_resource(ApiReaction, '/reaction/', '/reaction/<int:id>')
    api.add_resource(ApiUserReaction, '/user-reaction/<int:id>')
