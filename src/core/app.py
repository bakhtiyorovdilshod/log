import asyncio
from asyncio.log import logger

from fastapi import FastAPI, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from ..rabbitmq.client import PikaClient

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)


class LogApp(FastAPI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pika_client = PikaClient(self.log_incoming_message)

    @classmethod
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
    task = loop.create_task(log_app.pika_client.consume(loop))
    print(await task)
    await task


log_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)