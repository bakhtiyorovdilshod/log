from datetime import datetime


def validate_type(value, expected_type):
    if expected_type == 'string':
        return isinstance(value, str)
    elif expected_type == 'int':
        return isinstance(value, int)
    elif expected_type == 'float':
        return isinstance(value, float)
    elif expected_type == 'date':
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    else:
        return False


async def validate_rabbitmq_data(rabbit_data: dict, requirements: list):
    data = rabbit_data.get('data')
    count_fields = len(requirements)
    if count_fields == 0:
        return False
    for requirement in requirements:
        key = requirement['key']
        expected_type = requirement['type']
        if key in data:
            value = data[key]
            if validate_type(value, expected_type):
                count_fields -= 1
    if count_fields == 0:
        return True
    return False
