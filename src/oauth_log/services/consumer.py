import os, json

from src.oauth_log.schemas.consumer import OauthLogConsumerSchema
from src.rabbitmq.client import PikaClient


class OauthLogConsumer:
    """
        Oauth Log Consumer Class
    """
    def __init__(self):
        self.queue_name = os.environ.get('OAUTH_LOG_QUEUE_NAME', 'oauth_log')
        self.pika_client = PikaClient(self.log_incoming_message, self.queue_name)
        self.example_data = {
            "method": 'post',
            "table_name": 'user',
            "user_id": 10,
            "data": [
                {
                    "time": "2020-01-01"
                }
            ]
        }

    async def consumer(self, loop):
        await self.pika_client.consume(loop)

    async def producer(self):
         self.pika_client.send_message(dict(self.example_data))

    async def insert(self, message):
        pass

    @classmethod
    async def log_incoming_message(self, message: dict):
        """
            Method to do something meaningful with the incoming message
        """
        print(f'I consumed this message {message}')
