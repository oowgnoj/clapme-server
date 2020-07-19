import datetime
from jsonschema import ValidationError
from clapme.views.interface import Days


# time format validation
def validate_time(time: str):
    if len(time) != 4:
        raise ValidationError('time format error')
    if not time.isdigit():
        raise ValidationError('time format error')


# date string format validation
def validate_date_str(date_str: str):
    format = "%Y-%m-%d"
    try:
        datetime.datetime.strptime(date_str, format)
    except ValueError:
        raise ValidationError('dateStr format error')


# day format validation
def validate_day(day: str):
    if not Days.has_value(day):
        raise ValidationError('day format error')


# request schemas
signup_request = {
    'type': 'object',
    'properties': {
        'email': {'type': 'string'},
        'password': {'type': 'string'},
        'username': {'type': 'string'}
    },
    'required': [
        'email',
        'password'
    ]
}

login_request = {
    'type': 'object',
    'properties': {
        'email': {'type': 'string'},
        'password': {'type': 'string'}
    },
    'required': [
        'email',
        'password'
    ]
}

routine_post_request = {
    'type': 'object',
    'properties': {
        'title': {'type': 'string'},
        'alarm': {'type': 'boolean'},
        'time': {'type': 'string'},
        'mon': {'type': 'boolean'},
        'tue': {'type': 'boolean'},
        'wed': {'type': 'boolean'},
        'thu': {'type': 'boolean'},
        'fri': {'type': 'boolean'},
        'sat': {'type': 'boolean'},
        'sun': {'type': 'boolean'},
        'color': {'type': 'string'},
        'description': {'type': 'string'},
    },
    'required': [
        'title',
        'alarm',
        'time',
        'mon',
        'tue',
        'wed',
        'thu',
        'fri',
        'sat',
        'sun',
        'color'
    ]
}

routine_success_post_request = {
    'type': 'object',
    'properties': {
        'id': {'type': 'integer'},
        'dateStr': {'type': 'string'},
        'day': {'type': 'string'}
    },
    'required': [
        'id',
        'dateStr',
        'day'
    ]
}