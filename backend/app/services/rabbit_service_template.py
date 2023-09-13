from backend.app.database.mongodb import db
from bson.objectid import ObjectId

from backend.app.services.service_template import ServiceTemplate
from backend.app.utils.response import error_response_model


class RabbitServiceTemplate:
    def __init__(self):
        self.collection_name = 'rabbit_templates'
        self.service_collection = ServiceTemplate().collection_name

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
            return self.helper(service_query)

    async def list_templates(self):

        rabbit_list = []
        async for item in db.db[self.collection_name].find():
            rabbit_list.append(self.helper(item))
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

    async def get_rabbitmq_template(self, queue_name: str, table_name: str, method: str):
        requirement_fields = []
        service = await db.db[self.service_collection].find_one({
            'name': queue_name
        })
        if service:
            rabbit_template = await db.db[self.collection_name].find_one(
                {
                    'service_id': str(service.get('_id')),
                    'table_name': table_name
                }
            )
            if rabbit_template:
                validations = rabbit_template.get('validation')
                if len(validations) != 0:
                    fields = [validation.get('fields', []) for validation in validations if
                              validation.get('method') == method]
                    if len(fields) != 0:
                        requirement_fields = fields[0]
            return requirement_fields

    async def publisher_structure(self, service_name: str, table_name: str, method: str):
        response_data = {
            'table_name': table_name,
            'method': method,
            'user_id': 'int',
            'user_full_name': 'string',
            'data': {}
        }
        service = await db.db[self.service_collection].find_one({'name': service_name})
        if not service:
            return error_response_model(
                error='An error occurred',
                code=400,
                message=f"not found service that has name {service_name}"
            )
        rabbit_template = await db.db[self.collection_name].find_one(
            {
                'service_id': str(service.get('_id')),
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
                        x = {}
                        for field in fields[0]:
                            x.update({
                                f"{field.get('key')}": f"{field.get('type')}"
                            })
                        response_data['data'] = x

        return response_data


