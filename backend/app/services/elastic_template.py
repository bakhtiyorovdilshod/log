from bson import ObjectId

from backend.app.database.mongodb import db
from backend.app.utils.elastic_template import elastic_template_convertor
from backend.app.utils.response import error_response_model


class ElasticTemplateService:
    def __init__(self):
        self.collection_name = 'elastic_template'

    async def create_template(self, data: dict) -> dict:
        collection = self.get_collection()
        service = await db.db['rabbit_template'].find_one({'_id': ObjectId(data.get('service_id'))})
        if not service:
            return error_response_model(
                error='An error occurred',
                code=400,
                message=f"not found service that has id {data.get('service_id')}"
            )
        elastic_template = await collection.find_one({'table_name': str(data.get('table_name'))})
        if elastic_template:
            return error_response_model(
                error='An error occurred',
                code=400,
                message=f"there is already table {data.get('table_name')} template"
            )
        result = await collection.insert_one(data)
        return elastic_template_convertor(await collection.find_one({"_id": result.inserted_id}))

    async def update_template(self, id: str, data: dict) -> dict:
        collection = self.get_collection()
        template = await collection.find_one({'_id': ObjectId(id)})
        if not template:
            return error_response_model(
                error='An error occurred',
                code=400,
                message=f"not found template that has id {id}"
            )
        result = await collection.delete_one({'_id': ObjectId(id)})
        if result.deleted_count == 1:
            data.update({'service_id': template.get('service_id')})
            new_template = await collection.insert_one(data)
            return elastic_template_convertor(await collection.find_one({"_id": new_template.inserted_id}))
        return error_response_model(
            error='An error occurred',
            code=400,
            message=f"document that has id {id} not found or already deleted"
        )

    async def detail_template(self, id: str) -> dict:
        collection = self.get_collection()
        template = await collection.find_one({'_id': ObjectId(id)})
        if not template:
            return error_response_model(
                error='An error occurred',
                code=400,
                message=f"not found template that has id {id}"
            )
        return elastic_template_convertor(template)

    async def list_templates(self, service_id: str):
        result_templates = []
        collection = self.get_collection()
        filter_criteria = dict()
        if service_id:
            service = await db.db['rabbit_template'].find_one({'_id': ObjectId(service_id)})
            if not service:
                return error_response_model(
                    error='An error occurred',
                    code=400,
                    message=f"not found service that has id {service_id}"
                )
            filter_criteria.update({'service_id': service_id})
        async for template in collection.find(filter_criteria):
            result_templates.append(
                elastic_template_convertor(template)
            )
        return result_templates

    def get_collection(self):
        collection = db.db[self.collection_name]
        return collection


elastic_template_service = ElasticTemplateService()





