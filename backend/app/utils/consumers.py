import asyncio
from backend.app.utils.logger import logger_config

logger = logger_config(__name__)


async def consume_oauth_log(rabbitmq):
    rabbitmq.queue_name = 'oauth'
    rabbitmq.collection = 'oauth'
    rabbitmq.index_elastic = 'index-oauth'
    await rabbitmq.connect()
    while True:
        logger.info(f"Consuming data from {rabbitmq.queue_name} queue in RabbitMQ")
        await rabbitmq.consume(rabbitmq_instance=rabbitmq)


async def consume_state_log(rabbitmq):
    rabbitmq.queue_name = 'state'
    rabbitmq.collection = 'state'
    rabbitmq.index_elastic = 'index-state'
    await rabbitmq.connect()
    asyncio.ensure_future(rabbitmq.consume(rabbitmq_instance=rabbitmq))