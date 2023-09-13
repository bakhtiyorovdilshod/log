import json

from backend.app.utils.elastic import write_data_elastic
from backend.app.utils.mongodb import write_to_mongodb, get_rabbitmq_template
from backend.app.utils.rabbit import validate_rabbitmq_data


def write_log(method):
    async def wrapper(*args, **kwargs):
        rabbitmq_instance = kwargs.pop('rabbitmq_instance', None)
        result = await method(*args, **kwargs)
        collection = getattr(rabbitmq_instance, 'collection')
        index_elastic = getattr(rabbitmq_instance, 'index_elastic')
        rabbit_data = json.loads(result.body)
        requirements = await get_rabbitmq_template(rabbit_data, rabbitmq_instance.queue_name)
        status = await validate_rabbitmq_data(rabbit_data, requirements)
        if status:
            await write_to_mongodb(rabbit_data, collection)
            await write_data_elastic(index_elastic, json.loads(result.body))
        return result
    return wrapper
