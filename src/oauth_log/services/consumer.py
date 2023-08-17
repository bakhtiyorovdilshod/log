import os

from src.rabbitmq.client import PikaClient


class OauthLogConsumer:
    """
        Oauth Log Consumer Class
    """
    def __init__(self):
        self.queue_name = os.environ.get('OAUTH_LOG_QUEUE_NAME', 'oauth_log')

    async def consumer(self, loop):
        pika_client = await PikaClient(self.log_incoming_message, self.queue_name).consume(loop)

    async def insert(self, message):
        pass

    @classmethod
    async def log_incoming_message(self, message: dict):
        """
            Method to do something meaningful with the incoming message
        """
        print(f'I consumed this message {message}')
