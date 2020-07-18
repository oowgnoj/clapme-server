
# api.add_resource(ApiRoutine, '/routine')
#     api.add_resource(ApiRoutines, '/routines')
#     api.add_resource(ApiRoutineSuccess, '/routine-success')
#     api.add_resource(ApiRoutineMaterials, '/routine-materials')
#     api.add_resource(ApiIdea, '/idea')
import dataclasses
import json

from flask_restful import reqparse, abort, Api, Resource
from flask import request
from jsonschema import validate, ValidationError

from .interface import RoutineDto, routine_post_request
from ..models import db, User, Routine, Success, Color
from ..util.helper import decode_info, to_dict, extract, str_to_bool, validate_time, validate_date_str
from .auth import authenticate


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

        color = Color.query.filter_by(hex_code=json_data['color']).first()

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
        if 'day' in args and 'dateStr' in args:
            day = args['day']
            date_str = args['dateStr']

            try:
                validate_date_str(date_str)
            except ValidationError:
                abort(400)

            routines = ApiRoutines.get_daily_routines_with_status(user_id, day, date_str)
            return {'day': day, 'dateStr': date_str, 'routines': routines}, 200
        else:
            return ApiRoutines.get_all_routines(user_id), 200

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

        success_routine_id_list = map(lambda r: r.id, success_routine_list)

        result = []
        for routine in routine_list:
            routine = routine.convert_to_routine_status_dto()

            if routine['id'] in success_routine_id_list:
                routine['success'] = True

            result.append(routine)

        return result
