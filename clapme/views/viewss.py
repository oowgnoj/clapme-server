from flask_restful import reqparse, abort, Api, Resource


class ApiUserGoalList(Resource):
    def get(self, user_id):
        from models import Goal

        invited_goal_list = Goal.query.join(
            Goal.user_goals).filter_by(user_id=user_id, isAccepted=False).all()

        result = []
        for goal in invited_goal_list:
            invitation_info = {}
            invitation_info['user_goal_id'] = goal.user_goals[0].id
            invitation_info['title'] = goal.title
            result.append(invitation_info)

        return result


class ApiUserGoal(Resource):
    def delete(self, user_id, goal_id):
        from models import UserGoal
        from __init__ import db

        deleting_target = UserGoal.query.filter_by(
            user_id=user_id, goal_id=goal_id).first_or_404(description='해당 조건의 데이터가 존재하지 않습니다')

        db.session.delete(deleting_target)
        db.session.commit()
        return '성공적으로 삭제되었습니다', 200
