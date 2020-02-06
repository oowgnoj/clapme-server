from flask import request
from flask_restful import reqparse, abort, Api, Resource
from jwt import decode

SECRET_KEY = 'walnut'

parser = reqparse.RequestParser()
parser.add_argument('Authorization', location='headers')


# [helper 함수] 토큰 payload 에서 특정 키 attrs(type: list) 들의 값을 가져와 dict로 반환
def decode_info(token, attrs):
    result = {}
    decoded = jwt.decode(token, SECRET_KEY, algorithms='HS256')
    for attr in attrs:
        result[attr] = decoded[attr]
    return result


class ApiUserGoalList(Resource):
    def get(self):
        from models import Goal

        args = parser.parse_args()
        user_id = decoded_info(args['Authorization'], ['id'])
        # user_id = 3

        invited_goal_list = Goal.query.join(Goal.user_goals).filter_by(
            user_id=user_id, isAccepted=False).all()

        result = []

        for goal in invited_goal_list:
            invitation_info = {}
            invitation_info['user_goal_id'] = goal.user_goals[0].id
            invitation_info['goal_id'] = goal.id
            invitation_info['title'] = goal.title
            result.append(invitation_info)

        return result

    def post(self):
        from models import UserGoal
        from __init__ import db

        args = parser.parse_args()
        user_id = decoded_info(args['Authorization'], ['id'])

        json_data = request.get_json(force=True)
        # user_id = 3

        user_goal_new_connection = UserGoal(
            user_id=user_id, goal_id=json_data['goal_id'], subscribe=False, isAccepted=False)
        db.session.add(user_goal_new_connection)
        db.session.commit()

        return '성공적으로 추가되었습니다', 200

    def patch(self):
        from models import UserGoal
        from __init__ import db

        args = parser.parse_args()
        json_data = request.get_json(force=True)

        user_id = decoded_info(args['Authorization'], ['id'])
        # user_id = 3

        updating_target = UserGoal.query.filter_by(
            user_id=user_id, goal_id=json_data['goal_id']).first_or_404(description='해당 조건의 데이터가 존재하지 않습니다')

        print('updating_target', updating_target)

        if json_data.get('subscribe') != None:
            updating_target.subscribe = json_data['subscribe']
        if json_data.get('isAccepted') != None:
            updating_target.isAccepted = json_data['isAccepted']
        db.session.commit()

        return '성공적으로 수정되었습니다', 200


class ApiUserGoal(Resource):
    def delete(self, goal_id):
        from models import UserGoal
        from __init__ import db

        args = parser.parse_args()
        user_id = decoded_info(args['Authorization'], ['id'])

        deleting_target = UserGoal.query.filter_by(
            user_id=user_id, goal_id=goal_id).first_or_404(description='해당 조건의 데이터가 존재하지 않습니다')

        db.session.delete(deleting_target)
        db.session.commit()
        return '성공적으로 삭제되었습니다', 200
