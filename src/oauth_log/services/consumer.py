import os

from src.database import mongo_manager
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
                    "time": "2020-01-01",
                    "token": "83930023"
                }
            ]
        }

    async def consumer(self, loop):
        await self.pika_client.consume(loop)

    async def producer(self):
         self.pika_client.send_message(dict(self.example_data))

    async def insert(self, message):
        db = mongo_manager.db
        collection = db.oauth_logs
        collection.insert_one(message)

    async def log_incoming_message(self, message: dict):
        """
            Method to do something meaningful with the incoming message
        """
        print(f'I consumed this message {message}')
        await self.insert(message)
