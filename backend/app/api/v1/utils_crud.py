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


