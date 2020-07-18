

# api.add_resource(ApiRoutine, '/routine')
#     api.add_resource(ApiRoutines, '/routines')
#     api.add_resource(ApiRoutineSuccess, '/routine-success')
#     api.add_resource(ApiRoutineMaterials, '/routine-materials')
#     api.add_resource(ApiIdea, '/idea')

from flask_restful import reqparse, abort, Api, Resource
from flask import request
from jsonschema import validate, ValidationError

from .interface import RoutineDto, routine_post_request
from ..models import db,  Routine, Color
from ..util.helper import decode_info, to_dict, extract, str_to_bool, is_valid_time
from .auth import authenticate


parser = reqparse.RequestParser()


class ApiRoutine(Resource):
    method_decorators = [authenticate]

    # 특정 루틴 정보 조회
    def get(self, routine_id):
        routine = Routine.query.filter_by(id=routine_id).first()

        return RoutineDto(
            id=routine.id,
            title=routine.title,
            alarm=routine.alarm,
            time=routine.time,
            mon=routine.mon,
            tue=routine.tue,
            wed=routine.wed,
            thu=routine.thu,
            fri=routine.fri,
            sat=routine.sat,
            sun=routine.sun,
            color=routine.color.hex_code,
            description=routine.description
        ), 200

    # 루틴 생성
    def post(self):
        token = request.headers.get('Authorization')
        user_id = decode_info(token, ['id'])['id']

        json_data = request.get_json(force=True)

        try:
            validate(instance=json_data, schema=routine_post_request)
        except ValidationError:
            abort(400)

        if not is_valid_time(json_data['time']):
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


# class ApiRoutines(Resource):
#     method_decorators = [authenticate]
#
#     # 전체 루틴 목록 조회
#     def get(self):






