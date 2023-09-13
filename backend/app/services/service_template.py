from backend.app.database.mongodb import MongoManager
from fastapi.encoders import jsonable_encoder
from backend.app.database.mongodb import db
from bson.objectid import ObjectId
from bson import BSON


class ServiceTemplate:
    def __init__(self):
        self.collection_name = 'services'

    def get_collection(self):
        collection = db.db[self.collection_name]
        return collection

    def responseModel(self, data, message):
        return {
            "data": [data],
            "code": 200,
            "message": message
        }

    def service_template_helper(self, data) -> dict:
        return {
            "id": str(data['_id']),
            "name": data['name']
        }

    def error_response_model(self, error, code, message):
        return {
            'error': error,
            'code': code,
            'message': message
        }

    async def create_template(self, data: dict) -> dict:
        service_query = await self.get_collection().insert_one(data)
        template_query = await db.db[self.collection_name].find_one({'_id': service_query.inserted_id})
        return self.service_template_helper(template_query)

    async def retrieve_template(self, id: str):
        service_query = await db.db[self.collection_name].find_one({'_id': ObjectId(id)})
        if service_query:
            return self.service_template_helper(service_query)

    async def list_template(self):
        service_list = []
        async for item in db.db[self.collection_name].find():
            service_list.append(self.service_template_helper(item))
        return service_list

    async def update_template(self, id: str, data: str):
        if len(data) < 1:
            return False
        service_template = await db.db[self.collection_name].update_one({"_id": ObjectId(id)}, {"$set": data})
        if service_template:
            return True
        return False

    async def delete_template(self, id: str):
        service_template = await db.db[self.collection_name].find_one({"_id": ObjectId(id)})
        if service_template:
            await service_template.delete_one({"_id": ObjectId(id)})
            return True



