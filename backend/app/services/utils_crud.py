from backend.app.database.mongodb import MongoManager
from fastapi.encoders import jsonable_encoder
from backend.app.database.mongodb import db
from bson.objectid import ObjectId
from bson import BSON


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message
    }


def rabbit_template_helper(data) -> dict:
    return {
        "id": str(data['_id']),
        "name": data['name']
    }


async def create_template(data: dict) -> dict:
    service_query = await db.db['rabbit_template'].insert_one(data)
    template_query = await db.db['rabbit_template'].find_one({"_id": service_query.inserted_id})
    return rabbit_template_helper(template_query)


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
        return rabbit_template_helper(service_query)


async def retrieve_rabbit_template():
    rabbit_list = []
    async for item in db.db['rabbit_template'].find():
        rabbit_list.append(rabbit_template_helper(item))
    return rabbit_list


async def object_bson_name(name: str):
    bson_response = await db.db['rabbit_template'].find_one({"name": name})
    print(bson_response, "wwwww")


# --------------------------------------------  RabbitMQ Consumer template  -------------------------#


def rabbit_validation_helper(data) -> dict:
    return {
        "id": str(data['_id']),
        "queue_name": data['queue_name'],
        "table_name": data['table_name']}
        #   "validation": [
        #     {
        #       "method": data["method"],
        #       "fields": [
        #         {
        #           "key": data["key"],
        #           "type": data['type']
        #         }
        #       ]
        #     }
        #   ]
        # }


async def retrieve_template_validation_rabbit():
    """for rabbit validation data with validation"""
    rabbit_list = []
    async for item in db.db['Indexation_templates'].find():
        rabbit_list.append(rabbit_validation_helper(item))
    return rabbit_list


async def create_Indexation_templates(data: dict) -> dict:
    """RabbitMQ validation to mongodb create"""

    service_query = await db.db['Indexation_templates'].insert_one(data)
    template_query = await db.db['Indexation_templates'].find_one({"_id": service_query.inserted_id})
    return rabbit_validation_helper(template_query)


async def update_Indexation_templates(id: str, data: dict):
    if len(data) < 1:
        return False
    service_template = await db.db['Indexation_templates'].update_one({"_id": ObjectId(id)}, {"$set": data})
    if service_template:
        return True
    return False


async def delete_Indexation_templates(id: str):
    service_template = await db.db['Indexation_templates'].find_one({"_id": ObjectId(id)})
    if service_template:
        await service_template.delete_one({"_id": ObjectId(id)})
        return True


async def retrieve_event(id: str):
    service_query = await db.db['Indexation_templates'].find_one({"_id": ObjectId(id)})
    if service_query:
        return rabbit_template_helper(service_query)
