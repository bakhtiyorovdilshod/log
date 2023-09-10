from fastapi import FastAPI, APIRouter, Body, HTTPException
from backend.app.schemas.rabbitmq_template import (
    RabbitMQTemplateBase,
    RabbitMQTemplateById,
    RabbitConsumerBase
)
from backend.app.database.mongodb import db
from .utils_crud import (
    create_template,
    ResponseModel,
    rabbit_template_helper,
    update_template,
    delete_template,
    retrieve_template,
    retrieve_rabbit_template,
    object_bson_name,
    create_rabbit_consumer
)
from bson import ObjectId, json_util
from fastapi.encoders import jsonable_encoder


app = APIRouter()


@app.post("/create_rabbit_consumer")
async def create_consumer(data: RabbitConsumerBase = Body(...)):
    response = jsonable_encoder(data)
    response_object = await create_rabbit_consumer(response)
    return ResponseModel(response_object, "success")