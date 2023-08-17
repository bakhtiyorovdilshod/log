import asyncio, os
import json
from asyncio.log import logger

from fastapi import FastAPI, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from ..database import mongo_manager
from ..oauth_log.schemas.consumer import OauthLogConsumerSchema
from ..oauth_log.services.consumer import OauthLogConsumer
from ..rabbitmq.client import PikaClient
import nest_asyncio
from dotenv import load_dotenv
from src.oauth_log.routers.log import router as log_router
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


log_app.include_router(log_router, tags=["logs"], prefix="/api/v1")

router = APIRouter(
    tags=['items'],
    responses={404: {"description": "Page not found"}}
)

from pydantic import BaseModel


class MessageSchema(BaseModel):
    message: str


@router.post('/send-message')
async def send_message(payload: OauthLogConsumerSchema, request: Request):
    print(payload)
    request.app.pika_client.send_message(
        {"message": json.loads(payload.json())}
    )
    return {"status": "ok"}

log_app.include_router(prefix='/api/v1', router=router)


@log_app.on_event('startup')
async def startup():
    mongo_manager.connect_to_database(path=os.environ.get('MongoDB_URL'))
    loop = asyncio.get_running_loop()
    loop.run_until_complete(asyncio.gather(log_app.oauth_log.consumer(loop)))


@app.on_event("shutdown")
async def shutdown():
    await mongo_manager.close_database_connection()


log_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)