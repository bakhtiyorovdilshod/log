from backend.app.database.mongodb import MongoManager
from fastapi.encoders import jsonable_encoder
from backend.app.database.mongodb import db
from bson.objectid import ObjectId
from bson import BSON


class RabbitServiceTemplate:
    def __init__(self):
        self.collection_name = 'rabbit_templates'

    def helper(self, data) -> dict:
        return {
            "id": str(data['_id']),
            "service_id": data['service_id'],
            "table_name": data['table_name']

        }

    def responseModel(self,data, message):
        return {
            "data": [data],
            "code": 200,
            "message": message
        }

    def error_response_model(self,error, code, message):
        return {
            'error': error,
            'code': code,
            'message': message
        }
    def get_collection(self):
        collection = db.db[self.collection_name]
        return collection

    async def create_template(self, data: dict) -> dict:
        service_query = await db.db[self.collection_name].insert_one(data)
        template_query = await db.db[self.collection_name].find_one({"_id": service_query.inserted_id})
        return self.helper(template_query)

    async def retrieve_template(self, id:str):
        service_query = await db.db[self.collection_name].find_one({"_id": ObjectId(id)})
        if service_query:
            return helper(service_query)

    async def list_templates(self):

        rabbit_list = []
        async for item in db.db[self.collection_name].find():
            rabbit_list.append(helper(item))
        return rabbit_list

    async def update_templates(self, id: str, data: dict):
        if len(data) < 1:
            return False
        service_template = await db.db[self.collection_name].update_one({"_id": ObjectId(id)}, {"$set": data})
        if service_template:
            return True
        return False

    async def delete_templates(self, id: str):
        service_template = await db.db[self.collection_name].find_one({"_id": ObjectId(id)})
        if service_template:
            await service_template.delete_one({"_id": ObjectId(id)})
            return True

