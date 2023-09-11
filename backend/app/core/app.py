import asyncio
import json
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.database.mongodb import db
from dotenv import load_dotenv

from backend.app.core.rabbit import RabbitMQ
from backend.app.utils.consumers import consume_log

load_dotenv()

app = FastAPI()


@app.on_event('startup')
async def startup():
    await db.connect_to_database(path=os.environ.get('MongoDB_URL'))
    log = consume_log(queue_name='oauth', collection='oauth', index_elastic='index-oauth')
    task = asyncio.create_task(log)


@app.on_event("shutdown")
async def shutdown():
    await db.close_database_connection()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/publish/')
async def publish(data: dict):
    rabbitmq = RabbitMQ(url=os.environ.get('RABBIT_URL'))
    rabbitmq.queue_name = 'oauth'
    await rabbitmq.connect()
    data = json.dumps(data).encode('utf-8')
    await rabbitmq.publish(data)
    return {'message': data}