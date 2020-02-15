from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify, request, Flask, make_response


parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('description')
parser.add_argument('title')
parser.add_argument('interval')
parser.add_argument('times')
parser.add_argument('thumbnail')


class ApiGoal(Resource):
    def get(self, id):
        from clapme.models import Goal
        goal = Goal.query.filter_by(id=id).first()
        return {
            'id': goal.id,
            'description': goal.description,
            'interval': goal.interval,
            'times': goal.times
        }

    def post(self):
        from clapme.models import Goal
        from ..__init__ import db

        args = parser.parse_args()
        # primary key를 임시로 rows length 로 했는데, 어떤게 좋을지?
        rows = db.session.query(Goal).count() + 1

        description = args['description']
        title = args['title']
        interval = args['interval']
        times = args['times']
        thumbnail = args['thumbnail']

        NewGoal = Goal(id=rows, description=description, title=title,
                       interval=interval, times=times, thumbnail=thumbnail)

        # 만약 db에서 에러가 난다면?

        if NewGoal:
            db.session.add(NewGoal)
            db.session.commit()

        return make_response(jsonify({'title': title, 'description': description, 'interval': interval, 'times': times, 'thumbnail': thumbnail}), 200)

    def patch(self):
        from clapme.models import Goal
        from ..__init__ import db

        args = parser.parse_args()
        request_params = {'id': args['id'], 'description': args['description'], 'title': args['title'],
                          'interval': args['interval'], 'times': args['times'], 'thumbnail': args['thumbnail']}

        if not id:
            return '잘못된 id 입력값 입니다.', 400
        elif not (request_params['title'] or request_params['description'] or request_params['interval'] or request_params['times'] or request_params['thumbnail']):
            return '적어도 한가지 필드를 입력해 주세요', 400

        target = Goal.query.filter_by(id=id).first()
        for item in request_params:
            if request_params[item] != None:
                setattr(target, item, request_params[item])
                db.session.commit()

        return '성공적으로 변경되었습니다.'

    def delete(self):
        from clapme.models import Goal
        from ..__init__ import db

        args = parser.parse_args()
        id = args['id']

        if not id:
            return '잘못된 id 입력값 입니다.', 400

        target = Goal.query.filter_by(id=id).first()
        db.session.delete(target)
        db.session.commit()

        return '데이터가 성공적으로 삭제되었습니다.'

class ApiHistory(Resource):
    def get(self, id):
        from clapme.models import User, UserGoal
        from ..__init__ import db
        
        return '데이터가 성공적으로 삭제되었습니다.'


class ApiHistory(Resource):
    def get(self, id):
        from clapme.models import User, UserGoal
        from ..__init__ import db

        args = parser.parse_args()
        user_id = args['id']

        user_goal_list = UserGoal.query.filter_by(user_id=id).all()
        goal_success = []
        for user_goal in user_goal_list:
            success_list ={}
            success_list['user_id'] = user_goal.user_id
            success_list['user_name'] = user_goal.user.username
            success_list['goal_id'] = user_goal.goal.id
            for success in user_goal.goal.successes:
                success_list['success_id'] = success.id
                goal_success.append(success_list)
        return goal_success

class ApiReaction(Resource):
    def post(self):
        from clapme.models import Reaction
        from ..__init__ import db

        json_data = request.get_json(force=True)
        
        NewReaction = Reaction(user_id = json_data['user_id'], comment_id = json_data['comment_id'], type=json_data['type'] )
        db.session.add(NewReaction)
        db.session.commit()
        return json_data, 200

    def delete(self):
        from clapme.models import Reaction
        from ..__init__ import db

        args = parser.parse_args()
        id = args['id']

        target = Goal.query.filter_by(id=id).first()
        db.session.delete(target)
        db.session.commit()

        return '데이터가 성공적으로 삭제되었습니다.'

class ApiUserReaction(Resource):
    def get(self, id):
        from clapme.models import User, Success, Goal, Reaction
        from clapme.models import db

        user_success_reaction_list = []
        # print(Success.query.filter_by(id = id).first())
        user_success_list = Success.query.filter_by(user_id=id).all()
        for user_success in user_success_list:
            user_success_reaction = {}
            user_success_reaction['success_id'] = user_success.id
            # user_success_reaction['success_timestamp'] = user_success.id
            user_success_reaction['goal_id'] = user_success.goal_id
            user_success_reaction['goal_title'] = user_success.goal.title
            for success_reaction in user_success.reactions:
                user_success_reaction['user_id'] = success_reaction.user_id
                # user_success_reaction['user_name'] = success_reaction.User.user_name
                user_success_reaction['type'] = success_reaction.type
                user_success_reaction_list.append(user_success_reaction)
        
        return user_success_reaction_list, 200

class ApiReaction(Resource):
    def post(self):
        from clapme.models import Reaction
        from ..__init__ import db

        json_data = request.get_json(force=True)
        
        NewReaction = Reaction(user_id = json_data['user_id'], comment_id = json_data['comment_id'], type=json_data['type'] )
        db.session.add(NewReaction)
        db.session.commit()
        return json_data, 200

    def delete(self):
        from clapme.models import Reaction
        from ..__init__ import db

        args = parser.parse_args()
        id = args['id']

        target = Goal.query.filter_by(id=id).first()
        db.session.delete(target)
        db.session.commit()

        return '데이터가 성공적으로 삭제되었습니다.'
