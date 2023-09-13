from fastapi import APIRouter, Body, HTTPException, Depends
from backend.app.schemas.rabbitmq_template import (
    RabbitMQTemplateBase,
    RabbitConsumerBase,
    RabbitMQTemplateById,
    RabbitMQTemplateBase,
    ServiceId
)
from backend.app.database.mongodb import db
from backend.app.services.rabbit_service_template import RabbitServiceTemplate
from backend.app.services.service_template import ServiceTemplate
from bson import ObjectId, json_util
from fastapi.encoders import jsonable_encoder
import json

rabbit_template_router = APIRouter()
service_router = APIRouter()

# -------------------------------------------   Service  -----------------------------------------------#


@service_router.post("/")
async def create_service(data: RabbitMQTemplateBase = Body(...)):
    """rabbitmq service template creating"""
    service = ServiceTemplate()
    data = str(data.name)
    response_object = await service.get_collection().find_one({'name': data})
    if response_object:
        return service.error_response_model(error="An error occured", code=400, message=f"This is already existing")
    json_query = jsonable_encoder(name)
    service_query = await service.create_template(json_query)
    return service.responseModel(service_query, "Service name create added successfully")


@service_router.get("/{id}/")
async def get_service(id: str):
    """get by ObjectId service"""
    service = ServiceTemplate()
    object_id = ObjectId(id)
    response_object = await service.retrieve_template(id)
    data = await service.get_collection().find_one({"_id": object_id})

    if data is None:
        return service.error_response_model(error="An error occured", code=400, message=f"{id} not found")
    return service.responseModel(response_object, "successfully get object")


@service_router.get("/")
async def get_services():
    """get all services from database"""
    service = ServiceTemplate()
    response_object = await service.list_template()
    return service.responseModel(response_object, "Successfully get list of all services")


@service_router.delete("/{id}/")
async def delete_service(id: str):
    """delete service name"""
    service = ServiceTemplate()
    objectid = ObjectId(id)
    response_object = await service.get_collection().delete_one({'_id': objectid})
    if response_object.deleted_count == 0:
        return service.error_response_model(error="An error occured", code=400, message=f"{id} not found, please enter valid id")
    return {"status": 200, "message": "Service Name successfully deleted"}


@service_router.put("/{id}")
async def update_service(id: str, data: RabbitMQTemplateBase = Body(...)):

    service = ServiceTemplate()
    id = ObjectId(id)
    update_data = data.model_dump(exclude_none=True)
    result = await service.get_collection().update_one({"_id": id}, {"$set": update_data})
    error_result = await service.get_collection().find_one({"_id": id})
    if result.modified_count:
        return {"message": "Service Name has been updated"}
    elif error_result is None:
        return service.error_response_model(error="An error occured", code=400, message="Service not found!")


# ---------------------------------------   Rabbit Service   ----------------------------#


@rabbit_template_router.post("/")
async def create_rabbit_template(data: RabbitConsumerBase = Body(...)):
    """create rabbit validation"""
    rabbit_service = RabbitServiceTemplate()
    service = ServiceTemplate()
    queue = str(data.service_id)
    queue_id = ObjectId(data.service_id)
    response_object = await rabbit_service.get_collection().find_one({'service_id': queue})
    service = await service.get_collection().find_one({'_id': ObjectId(data.service_id)})
    if service is None:
        return rabbit_service.error_response_model(error="An error occurred", code=400, message="queue_id is incorrect , please create another one!")
    if response_object:
        return rabbit_service.error_response_model(error="An error occurred", code=400,
                                                  message=f"{queue_id} already existing, please create another one")

    response = jsonable_encoder(data)
    response_object = await rabbit_service.create_template(response)
    return rabbit_service.responseModel(response_object, "success")


@rabbit_template_router.get("/{id}/")
async def get_rabbit_template(id: str):
    rabbit_service = RabbitServiceTemplate()
    object_id = ObjectId(id)
    stores = {}
    data = await rabbit_service.get_collection().find_one({"_id": object_id})
    response = json.loads(json_util.dumps(data))
    stores.update(response)

    if data is None:
        return rabbit_service.error_response_model(error="an error occured", code=400, message="Data not found!")
    return rabbitservice.responseModel(stores, "successfully get object")


@rabbit_template_router.get("/")
async def get_all_rabbit_template():
    """get alla rabbit validation"""
    rabbit_service = RabbitServiceTemplate()
    stores = []
    response_objects = rabbit_service.get_collection().find()
    async for item in response_objects:
        response = json.loads(json_util.dumps(item))
        stores.append(response)
    return stores


@rabbit_template_router.put("/{id}/")
async def update_rabbit_template(id: str, data: RabbitConsumerBase = Body(...)):
    rabbit_service = RabbitServiceTemplate()
    id = ObjectId(id)
    update_data = data.model_dump(exclude_none=True)
    result = await rabbit_service.get_collection().update_one({"_id": id}, {"$set": update_data})
    error_result = await rabbit_service.get_collection().find_one({"_id": id})
    if result.modified_count:
        return {"message": "Event type model updated"}
    elif error_result is None:
        return rabbit_service.error_response_model(error="An error occured", code=400, message=f"This {id} service template not found")


@rabbit_template_router.delete("/{id}/")
async def delete_rabbit_template(id: str):
    rabbit_service = RabbitServiceTemplate()
    id = ObjectId(id)
    response_object = await rabbit_service.get_collection().delete_one({"_id": id})
    print(response_object, "ppppppp")
    if response_object.deleted_count == 0:
        return rabbit_service.error_response_model(error="An error not found!", code=400, message=f"{id} is not found!")
    return {"status": 200, "message": "Service Name successfully deleted"}



