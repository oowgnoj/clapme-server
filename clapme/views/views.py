from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify, request, Flask, make_response
from enum import Enum

from ..models import db, User, UserGoal, Goal, Routine, Success, Reaction, Comment, RoutineRecommend
from ..util.helper import decode_info, to_dict, extract, str_to_bool
from ..util.validation import api_json_validator
from .auth import authenticate
from datetime import date


parser = reqparse.RequestParser()


class ApiGoal(Resource):

    def get(self):
        token = request.headers.get('Authorization')
        user_id = decode_info(token, ['id'])['id']

        goal = Goal.query.filter_by(id=id).first()
        return {
            'id': goal.id,
            'description': goal.description,
            'interval': goal.interval,
            'times': goal.times,
            'title': goal.title,
            'thumbnail': goal.thumbnail,
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

        request_items = extract(
            json_data, ['id', 'description', 'interval', 'times', 'title', 'thumbnail'])
        Goal.query.filter_by(id=json_data['id']).update(request_items)

        return '성공적으로 변경되었습니다.'

    def delete(self, id):
        target = Goal.query.filter_by(id=id).first()
        db.session.delete(target)
        db.session.commit()
        return '데이터가 성공적으로 삭제되었습니다.'


# class ApiHistory(Resource):
#     def get(self, id):

#         user_goal_list = UserGoal.query.filter_by(user_id=id).all()
#         goal_success = []

#         for user_goal in user_goal_list:
#             success_list = {}
#             success_list['goal_id'] = user_goal.goal.id
#             success_list['goal_title'] = user_goal.goal.title
#             for success in user_goal.goal.successes:
#                 success_user = User.query.filter_by(id=success.user_id).first()
#                 success_list['success_id'] = success.id
#                 success_list['success_created'] = success.created.strftime(
#                     '%Y-%m-%d %H:%M:%S')
#                 success_list['success_user_id'] = success.user_id
#                 success_list['success_user_name'] = success_user.username
#                 success_list['success_user_profile'] = success_user.profile
#                 success_list['success_user_profile_pic'] = success_user.profile_pic
#                 goal_success.append(success_list)

#         return goal_success


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

        filter_option = {
            'user_id': user_id
        }

        user_goal_list_type = ('accepted', 'invited')
        args = request.args.get('type')

        if args == user_goal_list_type[0]:
            filter_option['isAccepted'] = True
        elif args == user_goal_list_type[1]:
            filter_option['isAccepted'] = False
        else:
            abort(400)

        goal_list = Goal.query.join('user_goals').filter_by(
            **filter_option).all()

        result = []

        for goal in goal_list:
            info = {}
            info['user_goal_id'] = goal.user_goals[0].id
            info['goal_id'] = goal.id
            info['title'] = goal.title
            result.append(info)

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
            user_id=user_id, goal_id=json_data['goal_id'], subscribe=False, isAccepted=False, is_owner=False)

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
        if json_data.get('is_owner') != None:
            updating_target.is_owner = json_data['is_owner']
        db.session.commit()

        return '성공적으로 수정되었습니다', 200

    def delete(self, goal_id):
        token = request.headers.get('Authorization')
        user_id = decode_info(token, ['id'])['id']

        deleting_target = UserGoal.query.filter_by(
            user_id=user_id, goal_id=goal_id).first_or_404(description='해당 조건의 데이터가 존재하지 않습니다')

        db.session.delete(deleting_target)
        db.session.commit()
        return '성공적으로 삭제되었습니다', 200


class ApiRoutineSuccess(Resource):
    def get(self, routine_id):
        result = []

        successes_of_goal = Success.query.filter_by(
            routine_id=routine_id).all()

        for success in successes_of_goal:
            success_info = {}
            success_info['id'] = success.id
            success_info['user_id'] = success.user_id
            success_info['user_name'] = success.user.username
            success_info['timestamp'] = success.created.strftime('%Y-%m-%d')
            success_info['reactions'] = []
            for reaction in success.reactions:
                reaction_info = {}
                reaction_info['id'] = reaction.id
                reaction_info['user_id'] = reaction.user.id
                reaction_info['user_name'] = reaction.user.username
                reaction_info['type'] = reaction.type
                success_info['reactions'].append(reaction_info)
            result.append(success_info)

        return result, 200

    def post(self):
        token = request.headers.get('Authorization')
        user_id = decode_info(token, ['id'])['id']

        json_data = request.get_json(force=True)

        try:
            api_json_validator(json_data, ['routine_id'])
        except Exception as error:
            abort(400, message="{}".format(error))

        new_success = Success(
            user_id=user_id, routine_id=json_data['routine_id'])
        db.session.add(new_success)
        db.session.commit()

        return '성공적으로 등록되었습니다.', 200


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
            comment_info['contents'] = comment.contents
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

    def post(self):
        token = request.headers.get('Authorization')
        user_id = decode_info(token, ['id'])['id']

        json_data = request.get_json(force=True)

        try:
            api_json_validator(json_data, ['goal_id', 'contents'])
        except Exception as error:
            abort(400, message="{}".format(error))

        new_comment = Comment(
            user_id=user_id, goal_id=json_data['goal_id'], contents=json_data['contents'])
        db.session.add(new_comment)
        db.session.commit()

        return '성공적으로 등록되었습니다.', 200

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

    def patch(self):
        token = request.headers.get('Authorization')
        user_id = decode_info(token, ['id'])['id']

        json_data = request.get_json(force=True)

        updating_info = extract(
            json_data, ['username', 'profile', 'profile_pic'])

        User.query.filter_by(id=user_id).update(updating_info)
        db.session.commit()

        return '성공적으로 수정되었습니다', 200


class ApiRoutine(Resource):

    def get(self, goal_id=None, day_of_week=None):
        if(goal_id == None):
            token = request.headers.get('Authorization')
            user_id = decode_info(token, ['id'])['id']
            if(day_of_week == None):
                user_routines = Routine.query.filter_by(user_id=user_id).all()
                res = []
                for user_routine in user_routines:
                    routine = to_dict(
                        user_routine, ['id', 'title', 'goal_id', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'time_at'])
                    res.append(routine)

                return res, 200

            else:
                user_routines = Routine.query.filter_by(user_id=user_id).all()
                res = []
                for user_routine in user_routines:
                    routine = to_dict(user_routine, [
                                      'id', 'title', 'goal_id', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'time_at'])
                    if routine[day_of_week]:
                        res.append(routine)

                return res, 200

        elif(goal_id != None):
            goal_routines = Routine.query.filter_by(goal_id=goal_id).all()
            res = []
            for goal_routine in goal_routines:
                routine = to_dict(goal_routine, [
                                  'id', 'title', 'goal_id', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'time_at'])
                res.append(routine)
            # res = getattr(goal_routine, 'title')
            return res, 200

    def post(self):
        json_data = request.get_json(force=True)

        token = request.headers.get('Authorization')
        user_id = decode_info(token, ['id'])['id']


        """ goal_id 는 임시로 body param에서 제외하고 post 요청 하고 있습니다 !"""
        # if json_data['goal_id'] is not None:
        #     new_routine = Routine(
        #         title=json_data['title'], user_id=json_data['user_id'], goal_id=json_data['goal_id'], mon=str_to_bool(json_data['mon']), tue=str_to_bool(json_data['tue']), wed=str_to_bool(json_data['wed']), thu=str_to_bool(json_data['thu']), fri=str_to_bool(json_data['fri']), sat=str_to_bool(json_data['sat']), sun=str_to_bool(json_data['sun']), time_at=json_data['time_at'])

        new_routine = Routine(
            title=json_data['title'], 
            user_id=user_id, 
            mon=str_to_bool(json_data['mon']), 
            tue=str_to_bool(json_data['tue']), 
            wed=str_to_bool(json_data['wed']), 
            thu=str_to_bool(json_data['thu']), 
            fri=str_to_bool(json_data['fri']), 
            sat=str_to_bool(json_data['sat']), 
            sun=str_to_bool(json_data['sun']), 
            time_at=json_data['time_at'])
        db.session.add(new_routine)
        db.session.commit()

        return '성공적으로 등록되었습니다.', 200

    def patch(self):
        json_data = request.get_json(force=True)

        request_items = extract(
            json_data, ['id', 'title', 'goal_id', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'time_at'])
        Routine.query.filter_by(id=json_data['id']).update(request_items)
        db.session.commit()

        return '성공적으로 변경되었습니다.'

    def delete(self, routine_id):
        target = Routine.query.filter_by(id=routine_id).first()
        db.session.delete(target)
        db.session.commit()
        return '데이터가 성공적으로 삭제되었습니다.'


class ApiRecommendList(Resource):
    def get(self):
        RoutineRecommendList = RoutineRecommend.query.all()
        res = []
        for routine in RoutineRecommendList:
            res.append(to_dict(routine, ['id', 'title']))

        return res, 200
