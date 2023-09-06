from aio_pika import connect_robust, Message
from dotenv import load_dotenv


from src.utils.decorator import write_log

load_dotenv()


class RabbitMQ:
    def __init__(self,  url):
        self.queue_name = None
        self.url = url
        self.connection = None
        self.channel = None
        self.queue = None
        self.collection = None
        self.index_elastic = None

    async def connect(self):
        self.connection = await connect_robust(self.url)
        self.channel = await self.connection.channel()
        self.queue = await self.channel.declare_queue(self.queue_name)

    @write_log
    async def consume(self, *args, **kwargs):
        async with self.queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    return message

    async def publish(self, message):
        await self.channel.default_exchange.publish(
            Message(body=message),
            routing_key=self.queue_name
        )
