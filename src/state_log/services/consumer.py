import os

from src.rabbitmq.client import PikaClient
from src.elasticsearch_log.elastic import BaseElasticSearch


class StateLogConsumer:
    """ State service data consumer"""

    def __init__(self):
        self.queue_name = os.environ.get('STATE_LOG_QUEUE_NAME')

    async def consumer(self, loop):
        pika_client = await PikaClient(self.log_income_message, self.queue_name).consume(loop)
        elastic_response = BaseElasticSearch()
        elastic_response = elastic_response.create_elastic(state, pika_client)

    async def insert(self, message):
        pass

    @classmethod
    async def log_income_message(self, message: dict):
        print(f'I consumed this message {message}')

