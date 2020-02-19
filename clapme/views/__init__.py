from flask_restful import Resource

from .views import ApiUserGoal, ApiGoalSuccessList, ApiGoalCommentList, ApiUser, ApiGoal, ApiHistory, ApiReaction, ApiUserReaction


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


def initialize_routes(api):
    api.add_resource(HelloWorld, '/')
    api.add_resource(ApiGoal, '/goal/', '/goal/<int:id>')
    api.add_resource(ApiUserGoal, '/user-goal/', '/user-goal/<int:goal_id>')
    api.add_resource(ApiGoalSuccessList, '/goal-success/<int:goal_id>')
    api.add_resource(ApiGoalCommentList, '/goal-comment/<int:goal_id>')
    api.add_resource(ApiUser, '/user/')
    api.add_resource(ApiHistory, '/history/<int:id>')
    api.add_resource(ApiReaction, '/reaction','/reaction/<int:id>')
    api.add_resource(ApiUserReaction, '/user-reaction/<int:id>')
