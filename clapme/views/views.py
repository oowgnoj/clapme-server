from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify, request, Flask, make_response

from clapme.models import db, User, UserGoal, Goal, Success, Reaction, Comment
from clapme.util.helper import decode_info, to_dict, extract
from clapme.util.validation import api_json_validator
from clapme.views.auth import authenticate

parser = reqparse.RequestParser()


class ApiGoal(Resource):

    def get(self, id):
        goal = Goal.query.filter_by(id=id).first()
        return {
            'id': goal.id,
            'description': goal.description,
            'interval': goal.interval,
            'times': goal.times
        }

    def post(self):
        token = request.headers.get('Authorization')
        user_id = decode_info(token, ['id'])['id']

        json_data = request.get_json(force=True)
        new_goal = Goal(description=json_data['description'], title=json_data['title'],
                        interval=json_data['interval'], times=json_data['times'], thumbnail=json_data['thumbnail'])

        db.session.add(new_goal)
        db.session.flush()
        db.session.refresh(new_goal)

        new_user_goal = UserGoal(
            user_id=user_id, goal_id=new_goal.id, subscribe=True, isAccepted=True, is_owner=True)

        db.session.add(new_user_goal)
        db.session.commit()

        return '데이터가 성공적으로 추가되었습니다', 200

    def patch(self):
        json_data = request.get_json(force=True)
        target = Goal.query.filter_by(id=json_data['id']).first()
        for item in json_data:
            if json_data[item] != None:
                setattr(target, item, json_data[item])
        db.session.commit()
        response = to_dict(
            target, ['title', 'description', 'interval', 'times', 'thumbnail'])
        return response, '성공적으로 변경되었습니다.'

    def delete(self, id):
        target = Goal.query.filter_by(id=id).first()
        db.session.delete(target)
        db.session.commit()
        return '데이터가 성공적으로 삭제되었습니다.'


class ApiHistory(Resource):
    def get(self, id):

        user_goal_list = UserGoal.query.filter_by(user_id=id).all()
        goal_success = []

        for user_goal in user_goal_list:
            success_list = {}
            success_list['goal_id'] = user_goal.goal.id
            success_list['goal_title'] = user_goal.goal.title
            for success in user_goal.goal.successes:
                success_user = User.query.filter_by(id=success.user_id).first()
                success_list['success_id'] = success.id
                success_list['success_created'] = success.created.strftime(
                    '%Y-%m-%d %H:%M:%S')
                success_list['success_user_id'] = success.user_id
                success_list['success_user_name'] = success_user.username
                success_list['success_user_profile'] = success_user.profile
                success_list['success_user_profile_pic'] = success_user.profile_pic
                goal_success.append(success_list)

        return goal_success


class ApiReaction(Resource):
    def post(self):
        json_data = request.get_json(force=True)

        NewReaction = Reaction(
            user_id=json_data['user_id'], comment_id=json_data['comment_id'], type=json_data['type'])
        db.session.add(NewReaction)
        db.session.commit()
        return '데이터가 성공적으로 추가되었습니다', 200

    def delete(self, id):

        target = Reaction.query.filter_by(id=id).first()
        db.session.delete(target)
        db.session.commit()
        return '데이터가 성공적으로 삭제되었습니다.'


class ApiUserReaction(Resource):
    def get(self, id):

        user_success_reaction_list = []

        user_success_list = Success.query.filter_by(user_id=id).all()
        for user_success in user_success_list:
            user_success_reaction = {}
            user_success_reaction['success_id'] = user_success.id
            user_success_reaction['success_timestamp'] = user_success.created.strftime(
                '%Y-%m-%d %H:%M:%S')
            user_success_reaction['goal_id'] = user_success.goal_id
            user_success_reaction['goal_title'] = user_success.goal.title
            for success_reaction in user_success.reactions:
                success_reaction_user = User.query.filter_by(
                    id=success_reaction.user_id).first()
                user_success_reaction['user_id'] = success_reaction.user_id
                user_success_reaction['type'] = success_reaction.type
                user_success_reaction['user_name'] = success_reaction_user.username
                user_success_reaction['user_profile_pic'] = success_reaction_user.profile_pic
                user_success_reaction_list.append(user_success_reaction)

        return user_success_reaction_list, 200


class ApiUserGoal(Resource):

    method_decorators = [authenticate]

    def get(self):
        token = request.headers.get('Authorization')
        user_id = decode_info(token, ['id'])['id']

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
        token = request.headers.get('Authorization')
        user_id = decode_info(token, ['id'])['id']

        json_data = request.get_json(force=True)

        try:
            api_json_validator(json_data, ['goal_id'])
        except Exception as error:
            abort(400, message="{}".format(error))

        user_goal_new_connection = UserGoal(
            user_id=user_id, goal_id=json_data['goal_id'], subscribe=False, isAccepted=False)

        db.session.add(user_goal_new_connection)
        db.session.commit()

        return '성공적으로 등록되었습니다.', 200

    def patch(self):
        token = request.headers.get('Authorization')
        user_id = decode_info(token, ['id'])['id']

        json_data = request.get_json(force=True)

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
        token = request.headers.get('Authorization')
        user_id = decode_info(token, ['id'])['id']
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

    method_decorators = [authenticate]

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

    method_decorators = [authenticate]

    def delete(self, comment_id):
        deleting_target = Comment.query.filter_by(
            id=comment_id).first_or_404(description='해당 조건의 데이터가 존재하지 않습니다')

        db.session.delete(deleting_target)
        db.session.commit()
        return '성공적으로 삭제되었습니다', 200


class ApiUser(Resource):

    method_decorators = [authenticate]

    def get(self):
        token = request.headers.get('Authorization')
        user_id = decode_info(token, ['id'])['id']

        user_info = User.query.filter_by(id=user_id).first()
        result = to_dict(
            user_info, ['id', 'email', 'username', 'profile_pic', 'profile'])

        return result, 200

    def post(self):
        token = request.headers.get('Authorization')
        user_id = decode_info(token, ['id'])['id']

        json_data = request.get_json(force=True)

        try:
            api_json_validator(json_data, ['email', 'password', 'username'])
        except Exception as error:
            abort(400, message="{}".format(error))

        signup_info = extract(
            json_data, ['email', 'password', 'username'])

        new_user = User(**signup_info)
        db.session.add(new_user)
        db.session.commit()

        return '성공적으로 등록되었습니다.', 200

    def patch(self):
        token = request.headers.get('Authorization')
        user_id = decode_info(token, ['id'])['id']

        json_data = request.get_json(force=True)

        updating_info = extract(
            json_data, ['username', 'profile', 'profile_pic'])

        User.query.filter_by(id=user_id).update(updating_info)
        db.session.commit()

        return '성공적으로 수정되었습니다', 200
