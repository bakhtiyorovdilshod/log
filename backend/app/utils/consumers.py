import asyncio
import os
from backend.app.core.consumer import RabbitMqConsumer
from backend.app.core.rabbit import RabbitMQ
from backend.app.utils.logger import logger_config

logger = logger_config(__name__)


async def consume_log(queue_name: str, collection: str, index_elastic: str):
    rabbitmq_instance = RabbitMQ(url=os.environ.get('RABBIT_URL'))
    consumer = RabbitMqConsumer(
        rabbitmq_instance=rabbitmq_instance,
        queue_name=queue_name,
        collection=collection,
        index_elastic=index_elastic
    )
    await consumer.start_consumer()

