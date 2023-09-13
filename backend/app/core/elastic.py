import asyncio
from elasticsearch import AsyncElasticsearch

from backend.app.services.elastic_template import elastic_template_service


class ElasticConfig:
    def __init__(self, host: str, username: str, password: str):
        self.host = host
        self.username = username
        self.password = password
        self.es = None

    async def connect(self):
        self.es = AsyncElasticsearch([self.host], http_auth=(self.username, self.password))

    async def save_data(self, index: str, body: dict):
        resp = await self.es.index(index=index, body=body)
        return resp

    async def search_data(self, index: str):
        resp = await self.es.search(index=index, body={'query': {'match_all': {}}}, size=200)
        return resp

    async def delete_data(self, index: str):
        self.es.delete_by_query(index=index, body={'query': {'match_all': {}}})

    async def reindex_data(self, mongo_data: list, index: str):
        actions = [
            {
                "_op_type": "index",
                "_index": index,
                "_source": document
            }
            for document in mongo_data
        ]

        await self.es.bulk(body=actions)

    async def generate_text(self):
        # templates = await elastic_template_service.get_templates(
        #     service_id=service_id,
        #     table_name=table_name,
        #     method=method
        # )
        pass

