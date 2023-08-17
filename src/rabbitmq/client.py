import json
import uuid
from asyncio.log import logger

import pika, os
import aio_pika
from dotenv import load_dotenv
load_dotenv()


class PikaClient:
    """
        Consuming data from other services
    """
    def __init__(self, process_callable, queue_name):
        """
            basic configuration for initializing pika client connection
        """
        # getting rabbitmq host
        self.host = os.environ.get('RABBIT_HOST', '127.0.0.1')
        self.port = os.environ.get('RABBIT_PORT', 5672)
        # getting queue name from .env
        self.publish_queue_name = queue_name
        # connecting rabbit host
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host)
        )
        # connecting rabbit channel
        self.channel = self.connection.channel()
        #  create queue with specific name
        self.publish_queue = self.channel.queue_declare(queue=self.publish_queue_name)

        self.callback_queue = self.publish_queue.method.queue
        self.response = None
        self.process_callable = process_callable
        print('Pika connection initialized')

    async def process_incoming_message(self, message):
        """
            Processing incoming message from RabbitMQ
        """
        await message.ack()
        body = message.body
        if body:
            await self.process_callable(json.loads(body))

    async def consume(self, loop):
        """
            Setup message listener with the current running loop
        """
        connection = await aio_pika.connect_robust(
            host=self.host,
            port=self.port,
            loop=loop
        )
        channel = await connection.channel()
        queue = await channel.declare_queue(self.publish_queue_name)
        await queue.consume(self.process_incoming_message, no_ack=False)
        print('Established pika async listener')
        return connection

    def send_message(self, message: dict):
        """
            Method to publish message to RabbitMQ
        """
        print(f'I produced that log: {message}')
        # publish message to the RabbitMQ
        self.channel.basic_publish(
            exchange='',
            routing_key=self.publish_queue_name,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=str(uuid.uuid4())
            ),
            body=json.dumps(message)
        )
