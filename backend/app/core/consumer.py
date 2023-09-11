from fastapi import Depends

from backend.app.core.rabbit import RabbitMQ
from backend.app.utils.logger import logger_config

logger = logger_config(__name__)


class RabbitMqConsumer:
    def __init__(self, rabbitmq_instance: Depends(RabbitMQ), queue_name: str, collection: str, index_elastic: str):
        self.rabbitmq_instance = rabbitmq_instance
        self.queue_name = queue_name
        self.collection = collection
        self.index_elastic = index_elastic
        self.asyncio_task = None

    async def start_consumer(self):
        self.rabbitmq_instance.queue_name = self.queue_name
        self.rabbitmq_instance.collection = self.collection
        self.rabbitmq_instance.index_elastic = self.index_elastic
        await self.rabbitmq_instance.connect()
        while True:
            logger.info(f"Consuming data from {self.queue_name} queue in RabbitMQ")
            await self.rabbitmq_instance.consume(rabbitmq_instance=self.rabbitmq_instance)

    async def stop_consumer(self):
        pass