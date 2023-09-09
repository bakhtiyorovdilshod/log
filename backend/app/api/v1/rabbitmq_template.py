from fastapi import FastAPI, APIRouter
from backend.app.schemas.rabbitmq_template import RabbitMQTemplateBase
from backend.app.database.mongodb import MongoManager
from fastapi.encoders import jsonable_encoder

app = APIRouter()


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message
    }


async def create_template(data: dict) -> dict:
    service_query = await db.db['rabbit_template'].insert_one(data)
    template_query = await db.db['rabbit_template'].find_one({"data": service_query})
    return template_query


async def update_template(id: str, data: dict):
    if len(data) < 1:
        return False
    service_template = await db.db['rabbit_template'].update_one({"_id": ObjectId(id)}, {"$set": data})
    if service_template:
        return True
    return False


async def delete_template(id: str):
    service_template = await db.db['rabbit_template'].find_one({"_id": ObjectId(id)})
    if service_template:
        await service_template.delete_one({"_id": ObjectId(id)})
        return True


async def retrieve_template(id: str):
    service_query = await db.db['rabbit_template'].find_one({"_id": ObjectId(id)})
    if service_query:
        return service_query


@app.post("/create")
async def create_template(name: RabbitMQTemplateBase):
    """rabbitmq service template creating"""

    json_query = jsonable_encoder(name)
    service_query = await create_template(json_query)
    return ResponseModel(service_query, "Service name create added successfully")

