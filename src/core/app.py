import asyncio
import json
import os
from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.database import db
from dotenv import load_dotenv

from src.core.rabbit import RabbitMQ
from src.utils.consumers import consume_oauth_log, consume_state_log

load_dotenv()

app = FastAPI()


@app.on_event('startup')
async def startup():
    rabbitmq = RabbitMQ(url=os.environ.get('RABBIT_URL'))
    await db.connect_to_database(path=os.environ.get('MongoDB_URL'))
    asyncio.create_task(consume_oauth_log(rabbitmq))
    # asyncio.create_task(consume_state_log(rabbitmq))


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