from flask import request
from flask_restful import reqparse, abort, Api, Resource

from clapme.models import db, User, UserGoal, Goal, Success, Reaction, Comment
from clapme.util.helper import to_dict, extract
from clapme.util.validation import api_json_validator

parser = reqparse.RequestParser()
parser.add_argument('Authorization', location='headers')


class ApiUserGoal(Resource):
    def get(self):
        args = parser.parse_args()
        user_id = decoded_info(args['Authorization'], ['id'])
        # user_id = 3

        invited_goal_list = Goal.query.join('user_goals').filter_by(
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
        args = parser.parse_args()
        user_id = decoded_info(args['Authorization'], ['id'])

        json_data = request.get_json(force=True)
        # user_id = 3

        try:
            api_json_validator(json_data, ['goal_id'])
        except Exception as error:
            abort(400, message="{}".format(error))

        user_goal_new_connection = UserGoal(
            user_id=user_id, goal_id=json_data['goal_id'], subscribe=False, isAccepted=False)

        db.session.add(user_goal_new_connection)
        db.session.commit()

        return '성공적으로 추가되었습니다', 200

    def patch(self):
        args = parser.parse_args()
        json_data = request.get_json(force=True)

        user_id = decoded_info(args['Authorization'], ['id'])
        # user_id = 3

        try:
            api_json_validator(json_data, ['goal_id'])
        except Exception as error:
            abort(400, message="{}".format(error))

        updating_target = UserGoal.query.filter_by(
            user_id=user_id, goal_id=json_data['goal_id']).first_or_404(description='해당 조건의 데이터가 존재하지 않습니다')

        if json_data.get('subscribe') != None:
            updating_target.subscribe = json_data['subscribe']
        if json_data.get('isAccepted') != None:
            updating_target.isAccepted = json_data['isAccepted']
        db.session.commit()

        return '성공적으로 수정되었습니다', 200

    def delete(self, goal_id):
        args = parser.parse_args()
        user_id = decoded_info(args['Authorization'], ['id'])
        # user_id = 3

        try:
            api_json_validator(json_data, ['goal_id'])
        except Exception as error:
            abort(400, message="{}".format(error))

        deleting_target = UserGoal.query.filter_by(
            user_id=user_id, goal_id=goal_id).first_or_404(description='해당 조건의 데이터가 존재하지 않습니다')

        db.session.delete(deleting_target)
        db.session.commit()
        return '성공적으로 삭제되었습니다', 200


class ApiGoalSuccessList(Resource):
    def get(self, goal_id):
        result = []

        successes_of_goal = Success.query.filter_by(goal_id=goal_id).all()

        for success in successes_of_goal:
            print('success', success)
            success_info = {}
            success_info['id'] = success.id
            success_info['user_id'] = success.user_id
            success_info['user_name'] = success.user.username
            success_info['timestamp'] = success.created.strftime('%Y-%m-%d')
            success_info['reactions'] = []
            for reaction in success.reactions:
                print('reaction', reaction)
                reaction_info = {}
                reaction_info['id'] = reaction.id
                reaction_info['user_id'] = reaction.user.id
                reaction_info['user_name'] = reaction.user.username
                reaction_info['type'] = reaction.type
                success_info['reactions'].append(reaction_info)
            result.append(success_info)

        return result, 200


class ApiGoalCommentList(Resource):
    def get(self, goal_id):
        result = []

        comments_of_goal = Comment.query.filter_by(goal_id=goal_id)

        for comment in comments_of_goal:
            comment_info = {}
            comment_info['id'] = comment.id
            comment_info['user_id'] = comment.user_id
            comment_info['goal_id'] = comment.goal_id
            comment_info['user_name'] = comment.user.username
            comment_info['content'] = comment.content
            comment_info['timestamp'] = comment.created.strftime('%Y-%m-%d')
            comment_info['reactions'] = []
            for reaction in comment.reactions:
                print('reaction', reaction)
                reaction_info = {}
                reaction_info['id'] = reaction.id
                reaction_info['user_id'] = reaction.user.id
                reaction_info['user_name'] = reaction.user.username
                reaction_info['type'] = reaction.type
                comment_info['reactions'].append(reaction_info)
            result.append(comment_info)

        return result, 200


class ApiGoalComment(Resource):

    def delete(self, comment_id):
        args = parser.parse_args()

        deleting_target = Comment.query.filter_by(
            id=comment_id).first_or_404(description='해당 조건의 데이터가 존재하지 않습니다')

        db.session.delete(deleting_target)
        db.session.commit()
        return '성공적으로 삭제되었습니다', 200


class ApiUser(Resource):

    def get(self):
        args = parser.parse_args()
        # user_id = decoded_info(args['Authorization'], ['id'])
        user_id = 1

        user_info = User.query.filter_by(id=user_id).first()
        result = to_dict(
            user_info, ['id', 'email', 'username', 'profile_pic', 'profile'])

        return result, 200

    def patch(self):
        args = parser.parse_args()
        json_data = request.get_json(force=True)

        # user_id = decoded_info(args['Authorization'], ['id'])
        user_id = 1

        updating_info = extract(
            json_data, ['username', 'profile', 'profile_pic'])

        db.session.query(User).filter(id == user_id).update(updating_info)
        db.session.commit()

        return '성공적으로 수정되었습니다', 200
