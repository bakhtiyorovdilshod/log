import asyncio
import os
from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.database import db
from dotenv import load_dotenv

from src.core.rabbit import RabbitMQ

load_dotenv()

app = FastAPI()
rabbitmq = RabbitMQ(queue_name='test', url=os.environ.get('RABBIT_URL'))


@app.on_event('startup')
async def startup():
    await db.connect_to_database(path=os.environ.get('MongoDB_URL'))
    await rabbitmq.connect()
    asyncio.ensure_future(rabbitmq.consume())


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


@app.post("/items/")
async def create_item(item: Dict):
    result = await db.db['log'].insert_one(item)
    return {"id": str(result.inserted_id)}


@app.get('/publish/{message}')
async def publish(message: str):
    await rabbitmq.publish(message)
    return {'message': message}