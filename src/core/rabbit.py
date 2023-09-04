import asyncio
import json

from aio_pika import connect_robust, Message

from src.core.elastic import ElasticConfig
from dotenv import load_dotenv
import os

load_dotenv()


class RabbitMQ:
    def __init__(self, queue_name, url):
        self.queue_name = queue_name
        self.url = url
        self.connection = None
        self.channel = None
        self.queue = None

    async def connect(self):
        self.connection = await connect_robust(self.url)
        self.channel = await self.connection.channel()
        self.queue = await self.channel.declare_queue(self.queue_name)

    async def consume(self):
        async with self.queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    print(message.body)
                    # x = ElasticConfig(host=os.environ.get('ELASTIC_HOST'), password='elastic', username='elastic')
                    # await x.connect()
                    # await x.save_data('test', body=json.loads(message.body))

    async def publish(self, message):
        await self.channel.default_exchange.publish(
            Message(body=message.encode()),
            routing_key=self.queue_name
        )
