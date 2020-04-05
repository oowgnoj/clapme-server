from jose import jwt

SECRET_KEY = 'coffee'


# [helper 함수] 토큰 payload 에서 특정 키 attrs(type: list) 들의 값을 가져와 dict로 반환
def decode_info(token, attrs):
    result = {}
    decoded = jwt.decode(token, SECRET_KEY, algorithms='HS256')
    for attr in attrs:
        result[attr] = decoded[attr]
    return result


# [helper 함수] DB 에서 불러온 리턴값인 query object 중 일부 필드만 객체로 추출
def to_dict(query, attrs):
    print(query, attrs)
    result = {}
    for attr in attrs:
        result[attr] = getattr(query, attr)

    return result


# [helper 함수] json 중 attrs 에 포함된 키만 객체로 추출
def extract(json, attrs):
    result = {}
    keys = json.keys()
    for key in keys:
        if key in attrs:
            result[key] = json[key]
    print('result', result)
    return result


def to_dict_nested(query, attrs, nested_attrs):
    result = {}
    for attr in attrs:
        value = getattr(query, attr)

        if(type(value) is list):
            result[attr] = to_dict(value, nested_attrs)
        else:
            result[attr] = getattr(query, attr)
    return result


# [helper 함수] sting -> boolean
def str_to_bool(s):
    if s == 'True':
        return True
    elif s == 'False':
        return False
    else:
        raise ValueError
