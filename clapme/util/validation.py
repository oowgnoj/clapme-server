# body 에 필수 항목이 다 포함되어 있는지 확인
class RequiredException(Exception):
    pass


def api_json_validator(json, required_keys):
    data_keys = json.keys()
    print('data_keys', data_keys)

    for required_key in required_keys:
        if required_key not in data_keys:
            raise RequiredException("[{}] 항목은 필수 항목입니다.".format(required_key))
