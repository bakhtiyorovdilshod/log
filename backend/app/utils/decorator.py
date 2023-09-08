import json

from backend.app.utils.elastic import write_data_elastic
from backend.app.utils.mongodb import write_to_mongodb


def write_log(method):
    async def wrapper(*args, **kwargs):
        rabbitmq_instance = kwargs.pop('rabbitmq_instance', None)
        result = await method(*args, **kwargs)
        collection = getattr(rabbitmq_instance, 'collection')
        index_elastic = getattr(rabbitmq_instance, 'index_elastic')
        await write_to_mongodb(json.loads(result.body), collection)
        await write_data_elastic(index_elastic, json.loads(result.body))
        return result
    return wrapper
