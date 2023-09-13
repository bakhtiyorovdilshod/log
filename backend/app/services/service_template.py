from backend.app.database.mongodb import db
from bson.objectid import ObjectId
from backend.app.utils.response import error_response_model


class ServiceTemplate:

    def __init__(self):
        self.collection_name = 'services'
        self.rabbit_template_collection = None

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

    async def attributes(self, table_name: str, service_id: str, method: str):
        from backend.app.services.rabbit_service_template import RabbitServiceTemplate
        self.rabbit_template_collection = RabbitServiceTemplate().collection_name
        requirement_fields = []
        service = await db.db[self.collection_name].find_one({"_id": ObjectId(service_id)})
        if not service:
            return error_response_model(
                error='An error occurred',
                code=400,
                message=f"not found service that has id {service_id}"
            )
        rabbit_template = await db.db[self.rabbit_template_collection].find_one(
            {
                'service_id': service_id,
                'table_name': table_name
            }
        )
        if rabbit_template:
            validations = rabbit_template.get('validation', [])
            if len(validations) != 0:
                validations = rabbit_template.get('validation')
                if len(validations) != 0:
                    fields = [validation.get('fields', []) for validation in validations if
                              validation.get('method') == method]
                    if len(fields) != 0:
                        requirement_fields = fields[0]
        return requirement_fields





