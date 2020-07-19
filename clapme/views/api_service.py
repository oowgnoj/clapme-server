import random
from flask_restful import reqparse, abort, Resource
from flask import request
from jsonschema import validate, ValidationError

from ..models import db, Routine, Success, Color, Idea
from ..util.constant import color_sets

from .api_auth import authenticate, decode_info
from .validation import validate_time, validate_day, validate_date_str, \
    routine_post_request, routine_success_post_request

parser = reqparse.RequestParser()


class ApiRoutine(Resource):
    method_decorators = [authenticate]

    # 특정 루틴 정보 조회
    def get(self, routine_id):
        routine = Routine.query.filter_by(id=routine_id).first()
        return routine.convert_to_routine_dto(), 200

    # 루틴 생성
    def post(self):
        token = request.headers.get('Authorization')
        user_id = decode_info(token, ['id'])['id']

        json_data = request.get_json(force=True)

        try:
            validate(instance=json_data, schema=routine_post_request)
            validate_time(json_data['time'])
        except ValidationError:
            abort(400)

        description = ''
        if 'description' in json_data:
            description = json_data['description']

        color = Color.query\
            .filter_by(hex_code=json_data['color'])\
            .first()

        new_routine = Routine(
            user_id=user_id,
            title=json_data['title'],
            mon=json_data['mon'],
            tue=json_data['tue'],
            wed=json_data['wed'],
            thu=json_data['thu'],
            fri=json_data['fri'],
            sat=json_data['sat'],
            sun=json_data['sun'],
            alarm=json_data['alarm'],
            time=json_data['time'],
            description=description,
            color_id=color.id
        )

        db.session.add(new_routine)
        db.session.commit()

        json_data['id'] = new_routine.id
        return json_data, 200


class ApiRoutines(Resource):
    method_decorators = [authenticate]

    def get(self):
        token = request.headers.get('Authorization')
        user_id = decode_info(token, ['id'])['id']

        args = request.args
        is_daily_list_request = 'day' in args and 'dateStr' in args

        if is_daily_list_request:
            day = args['day']
            date_str = args['dateStr']

            try:
                validate_day(day)
                validate_date_str(date_str)
            except ValidationError:
                abort(400)

            routines = ApiRoutines.get_daily_routines_with_status(
                user_id,
                day,
                date_str
            )
            return {'day': day,
                    'dateStr': date_str,
                    'routines': routines}, 200
        else:
            return ApiRoutines.get_all_routines(
                user_id
            ), 200

    # 루틴 전체 목록 조회
    @staticmethod
    def get_all_routines(user_id: str):
        filter_option = {'user_id': user_id}

        routine_list = Routine.query\
            .filter_by(**filter_option)\
            .order_by(Routine.time.asc())\
            .all()

        result = []
        for routine in routine_list:
            result.append(routine.convert_to_routine_dto())

        return result

    # 오늘자 루틴 목록 조회 (수행 여부 포함)
    @staticmethod
    def get_daily_routines_with_status(user_id: str, day: str, date_str: str):
        routine_filter_option = {'user_id': user_id, day: True}
        success_filter_option = {'day': day, 'date_str': date_str}

        routine_list = Routine.query\
            .filter_by(**routine_filter_option)\
            .order_by(Routine.time.asc())\
            .all()

        success_routine_list = Routine.query\
            .filter_by(**routine_filter_option)\
            .join(Success)\
            .filter_by(**success_filter_option)\
            .all()

        success_routine_id_list = list(map(lambda r: r.id, success_routine_list))

        result = []
        for routine in routine_list:
            routine = routine.convert_to_routine_status_dto()

            if routine['id'] in success_routine_id_list:
                routine['success'] = True

            result.append(routine)

        return result


class ApiRoutineSuccess(Resource):
    method_decorators = [authenticate]

    def post(self):
        token = request.headers.get('Authorization')
        user_id = decode_info(token, ['id'])['id']

        json_data = request.get_json(force=True)

        try:
            validate(instance=json_data, schema=routine_success_post_request)
            validate_day(json_data['day'])
            validate_date_str(json_data['dateStr'])
        except ValidationError:
            abort(400)

        new_success = {
            'routine_id': json_data['id'],
            'day': json_data['day'],
            'date_str': json_data['dateStr']
        }

        if Success.query.filter_by(**new_success).first() is not None:
            abort(409)

        db.session.add(Success(**new_success))
        db.session.commit()

        return ApiRoutines.get_daily_routines_with_status(
            user_id,
            json_data['day'],
            json_data['dateStr']
        ), 200


class ApiRoutineMaterials(Resource):
    method_decorators = [authenticate]

    def get(self):
        main_colors = Color.query.order_by(Color.id).all()

        colors = []
        for main in main_colors:
            main_hex_code = main.hex_code

            colors.append({
                'main': main_hex_code,
                'sub': color_sets[main_hex_code]
            })

        return {'colors': colors}, 200


class ApiIdea(Resource):
    method_decorators = [authenticate]

    def get(self):
        request_type = request.args['type']
        idea_list = Idea.query.order_by(Idea.id).all()

        if request_type == 'random':
            random_index = random.randint(0, len(idea_list)-1)
            random_idea = idea_list[random_index]
            return random_idea.convert_to_routine_sample_dto(), 200

        elif request_type == 'list':
            return list(map(lambda idea: idea.convert_to_routine_sample_dto(), idea_list)), 200

        else:
            abort(400)












