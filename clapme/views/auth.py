from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify, request, Flask, make_response
from jose import jwt
from functools import wraps

from ..models import db, User, UserGoal, Goal, Success, Reaction, Comment
from ..util.helper import to_dict, extract
from ..util.validation import api_json_validator


key = 'coffee'


class ApiLogin(Resource):
    def post(self):
        json_data = request.get_json(force=True)

        email = json_data['email']
        password = json_data['password']

        user_info = User.query.filter_by(email=email).first()

        payload = {
            'id': user_info.id,
            'username': user_info.username,
            'email': user_info.email,
            'profile': user_info.profile,
            'profile_pic': user_info.profile_pic
        }

        encoded = jwt.encode(payload, key, algorithm='HS256')
        result = {'access-token': encoded, 'username': user_info.username, 'email': user_info.email,
                  'profile': user_info.profile, 'profile_pic': user_info.profile_pic}
        return result, 200


class ApiSignup(Resource):
    def post(self):
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


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # if not getattr(func, 'authenticated', True):
        # return func(*args, **kwargs)

        parser = reqparse.RequestParser()
        parser.add_argument('Authorization', location='headers')
        token = parser.parse_args()

        # custom account lookup function

        if token['Authorization'] != None:
            print('통과가 되었다는거니?')
            return func(*args, **kwargs)

        abort(401)
    return wrapper
