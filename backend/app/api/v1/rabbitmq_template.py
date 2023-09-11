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
    update_Indexation_templates,
    retrieve_event
)
from bson import ObjectId, json_util
from fastapi.encoders import jsonable_encoder
import json

rabbit_template_router = APIRouter()
service_router = APIRouter()

# -------------------------------------------   API CRUD  -----------------------------------------------#


@service_router.post("/")
async def create_service(name: RabbitMQTemplateBase = Depends()):
    """rabbitmq service template creating"""

    names = str(name.name)
    response_object = await db.db['rabbit_template'].find_one({'name': names})
    if response_object:
        raise HTTPException(status_code=400, detail="already existing")
    json_query = jsonable_encoder(name)
    service_query = await create_template(json_query)
    return ResponseModel(service_query, "Service name create added successfully")


@service_router.get("/{id}/")
async def get_service(id: str):
    """get by ObjectId service"""
    object_id = ObjectId(id)
    response_object = await retrieve_template(id)
    data = await db.db['rabbit_template'].find_one({"_id": object_id})

    if data is None:
        raise HTTPException(status_code=404, detail="Data not found")
    return ResponseModel(response_object, "successfully get object")


@service_router.get("/")
async def get_services():
    """get all services from database"""

    response_object = await retrieve_rabbit_template()
    return ResponseModel(response_object, "Successfully get list of all services")


@service_router.delete("/{id}/")
async def delete_service(id: str):
    """delete service name"""
    objectid = ObjectId(id)
    response_object = await db.db['rabbit_template'].delete_one({'_id': objectid})
    if response_object.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"status": 200, "message": "Service Name successfully deleted"}


@service_router.put("/{id}")
async def update_service(id: str, data: RabbitMQTemplateBase = Body(...)):
    id = ObjectId(id)
    update_data = data.model_dump(exclude_none=True)
    result = await db.db['rabbit_template'].update_one({"_id": id}, {"$set": update_data})
    error_result = await db.db['rabbit_template'].find_one({"_id": id})
    if result.modified_count:
        return {"message": "Service Name has been updated"}
    elif error_result is None:
        raise HTTPException(status_code=404, detail="Service name model not found!")

# ---------------------------------------   Rabbit Consumer mongodb create  ----------------------------#


@rabbit_template_router.post("/")
async def create_rabbit_template(data: RabbitConsumerBase = Body(...)):
    """create rabbit validation"""

    queue_name = str(data.queue_name)
    response_object = await db.db['Indexation_templates'].find_one({'queue_name': queue_name})
    if response_object:
        raise HTTPException(status_code=400, detail=f" {queue_name} already existing, please create another one!")
    response = jsonable_encoder(data)
    response_object = await create_Indexation_templates(response)
    return ResponseModel(response_object, "success")


@rabbit_template_router.get("/{id}/")
async def get_rabbit_template(id: str):
    object_id = ObjectId(id)
    stores = {}
    data = await db.db['Indexation_templates'].find_one({"_id": object_id})
    response = json.loads(json_util.dumps(data))
    stores.update(response)

    if data is None:
        raise HTTPException(status_code=404, detail="Data not found")
    return ResponseModel(stores, "successfully get object")


@rabbit_template_router.get("/")
async def get_all_rabbit_template():
    """get alla rabbit validation"""

    stores = []
    response_objects = db.db['Indexation_templates'].find()
    async for item in response_objects:
        response = json.loads(json_util.dumps(item))
        stores.append(response)
    return stores


@rabbit_template_router.put("/{id}/")
async def update_rabbit_template(id: str, data: RabbitConsumerBase = Body(...)):
    id = ObjectId(id)
    update_data = data.model_dump(exclude_none=True)
    result = await db.db['Indexation_templates'].update_one({"_id": id}, {"$set": update_data})
    error_result = await db.db['Indexation_templates'].find_one({"_id": id})
    if result.modified_count:
        return {"message": "Event type model updated"}
    elif error_result is None:
        raise HTTPException(status_code=404, detail="Event type model not found!")


@rabbit_template_router.delete("/{id}/")
async def delete_rabbit_template(id: str):
    id = ObjectId(id)
    response_object = await db.db['Indexation_templates'].delete_one({"_id": id})
    print(response_object, "ppppppp")
    if response_object.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"status": 200, "message": "Service Name successfully deleted"}



