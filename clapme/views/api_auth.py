import config
from flask_restful import reqparse, abort, Resource
from flask import request
from jose import jwt
from functools import wraps
from jsonschema import validate, ValidationError

from .validation import login_request, signup_request
from ..models import db, User
from ..util import extract


secret = config.JWT_SECRET_KEY


class ApiLogin(Resource):
    def post(self):
        json_data = request.get_json(force=True)

        try:
            validate(instance=json_data, schema=login_request)
        except ValidationError:
            abort(400)

        email = json_data['email']
        password = json_data['password']

        user_info = User.query.filter_by(email=email).first()

        if password != user_info.password:
            abort(401)

        payload = {
            'id': user_info.id,
            'username': user_info.username,
            'email': user_info.email,
            'profile': user_info.profile,
            'pic_url': user_info.pic_url
        }

        encoded = jwt.encode(payload, secret, algorithm='HS256')
        result = {'accessToken': encoded, 'username': user_info.username}
        return result, 200


class ApiSignup(Resource):
    def post(self):
        json_data = request.get_json(force=True)

        try:
            validate(instance=json_data, schema=signup_request)
        except ValidationError:
            abort(400)

        email = json_data['email']
        password = json_data['password']
        username = email.split("@")[0] # username 이 없을 경우 (oauth 등) email 의 아이디를 username 으로 설정

        if username in json_data:
            username = json_data['username']

        new_user = User(
            email=email,
            password=password,
            username=username
        )
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
        if token['Authorization'] is not None:
            return func(*args, **kwargs)

        abort(401)

    return wrapper


def decode_info(token, attrs):
    result = {}
    decoded = jwt.decode(token, secret, algorithms='HS256')
    for attr in attrs:
        result[attr] = decoded[attr]
    return result
