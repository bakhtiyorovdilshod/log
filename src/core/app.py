import asyncio, os
from asyncio.log import logger

from fastapi import FastAPI, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from ..database import db
from ..oauth_log.services.consumer import OauthLogConsumer
from ..rabbitmq.client import PikaClient
import nest_asyncio
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

# 👇️ call apply()
nest_asyncio.apply()

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)


class LogApp(FastAPI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pika_client = PikaClient(self.log_incoming_message, 'oauth_log')
        self.oauth_log = OauthLogConsumer()

    # @classmethod
    def log_incoming_message(cls, message: dict):
        """Method to do something meaningful with the incoming message"""
        logger.info('Here we got incoming message %s', message)


log_app = LogApp()

router = APIRouter(
    tags=['items'],
    responses={404: {"description": "Page not found"}}
)

from pydantic import BaseModel


class MessageSchema(BaseModel):
    message: str


@router.post('/send-message')
async def send_message(payload: MessageSchema, request: Request):
    request.app.pika_client.send_message(
        {"message": payload.message}
    )
    return {"status": "ok"}

log_app.include_router(prefix='/api/v1', router=router)


@log_app.on_event('startup')
async def startup():
    loop = asyncio.get_running_loop()
    loop.run_until_complete(asyncio.gather(log_app.oauth_log.consumer(loop), log_app.oauth_log.producer()))
    db.connect_to_database(path=os.environ.get('MongoDB_URL'))


@app.on_event("shutdown")
async def shutdown():
    await db.close_database_connection()


log_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)