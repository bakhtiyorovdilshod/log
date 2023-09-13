import json

from backend.app.utils.mongodb import write_to_mongodb_and_elastic


def write_log(method):
    async def wrapper(*args, **kwargs):
        rabbitmq_instance = kwargs.pop('rabbitmq_instance', None)
        result = await method(*args, **kwargs)
        collection = getattr(rabbitmq_instance, 'collection')
        index_elastic = getattr(rabbitmq_instance, 'index_elastic')
        rabbit_data = json.loads(result.body)
        await write_to_mongodb_and_elastic(
            queue_name=rabbitmq_instance.queue_name,
            rabbit_data=rabbit_data,
            collection=collection,
            index_elastic=index_elastic)
        return result
    return wrapper
