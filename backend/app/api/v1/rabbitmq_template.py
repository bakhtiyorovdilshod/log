from fastapi import APIRouter, Body, HTTPException, Depends
from backend.app.schemas.rabbitmq_template import (
    RabbitMQTemplateBase,
    RabbitConsumerBase,
    RabbitMQTemplateById,
    RabbitMQTemplateBase
)
from backend.app.database.mongodb import db
from backend.app.services.utils_crud import (
    create_template,
    ResponseModel,
    retrieve_template,
    retrieve_rabbit_template,
    create_Indexation_templates,
    update_Indexation_templates
)
from bson import ObjectId, json_util
from fastapi.encoders import jsonable_encoder
import json

app = APIRouter()


# -------------------------------------------   API CRUD  -----------------------------------------------#


@app.post("/create")
async def create_templates(name: RabbitMQTemplateBase = Depends()):
    """rabbitmq service template creating"""

    names = str(name)
    response_object = await db.db['rabbit_template'].find_one({'name': names})
    if response_object:
        raise HTTPException(status_code=400, detail="already existing")
    json_query = jsonable_encoder(name)
    service_query = await create_template(json_query)
    return ResponseModel(service_query, "Service name create added successfully")


@app.get("/get_service/{id}/")
async def get_service(id: str):
    """get by ObjectId service"""
    object_id = ObjectId(id)
    response_object = await retrieve_template(id)
    data = await db.db['rabbit_template'].find_one({"_id": object_id})

    if data is None:
        raise HTTPException(status_code=404, detail="Data not found")
    return ResponseModel(response_object, "successfully get object")


@app.get("/all_services/")
async def get_services():
    """get all services from database"""

    response_object = await retrieve_rabbit_template()
    return ResponseModel(response_object, "Successfully get list of all services")


@app.delete("/service{id}/")
async def delete_service_name(id: str):
    """delete service name"""
    objectid = ObjectId(id)
    response_object = await db.db['rabbit_template'].delete_one({'_id': objectid})
    if response_object.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"status": 200, "message": "Service Name successfully deleted"}


# ---------------------------------------   Rabbit Consumer mongodb create  ----------------------------#


@app.post("/create_event/")
async def create_Indexation_template(data: RabbitConsumerBase = Body(...)):
    """create rabbit validation"""

    queue_name = str(data.queue_name)
    response_object = await db.db['Indexation_templates'].find_one({'queue_name': queue_name})
    if response_object:
        raise HTTPException(status_code=400, detail=f" {queue_name} already existing, please create another one!")
    response = jsonable_encoder(data)
    response_object = await create_Indexation_templates(response)
    return ResponseModel(response_object, "success")


@app.get("/all_event/")
async def get_all_Indexation_templates():
    """get alla rabbit validation"""

    stores = []
    response_objects = db.db['Indexation_templates'].find()
    async for item in response_objects:
        response = json.loads(json_util.dumps(item))
        stores.append(response)
    return stores


@app.put("/event{id}/")
async def update_Indexation_templates(id: str, data: RabbitConsumerBase = Body(...)):
    # id = ObjectId(id)
    request = {k: v for k, v in data.model_dump().items() if v is not None}
    updated_validation = await update_Indexation_templates(id, data)
    update_data = data.model_dump()


@app.delete("/event{id}/")
async def delete_Indexation_templates(id: str):
    id = ObjectId(id)
    response_object = await db.db['Indexation_templates'].delete_one({"_id": id})
    if response_object.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"status": 200, "message": "Service Name successfully deleted"}



