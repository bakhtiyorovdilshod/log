from fastapi import FastAPI, APIRouter, Body, HTTPException
from backend.app.schemas.rabbitmq_template import (
    RabbitMQTemplateBase,
    RabbitMQTemplateById,
    RabbitConsumerBase,
    RabbitConsumerValidationBase,
    RabbitConsumerFields,

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
    create_rabbit_consumer,
    retrieve_rabbit_consumer,

)
from bson import ObjectId, json_util
from fastapi.encoders import jsonable_encoder


app = APIRouter()


@app.post("/create_rabbit_consumer")
async def create_consumer(data: RabbitConsumerBase = Body(...)):
    print("pppppp")
    response = jsonable_encoder(data)
    response_object = await create_rabbit_consumer(response)
    return ResponseModel(response_object, "success")


@app.get("/get_all_rabbit_consumer")
async def get_all_consumer():
    response_object = await retrieve_rabbit_consumer()
    return ResponseModel(response_object, "get all rabbit consumer data")
