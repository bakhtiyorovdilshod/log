import asyncio
from elasticsearch import AsyncElasticsearch


class ElasticConfig:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.es = None

    async def connect(self):
        self.es = AsyncElasticsearch([self.host], http_auth=(self.username, self.password))

    async def save_data(self, index, body):
        resp = await self.es.index(index=index, body=body)

        return resp

    async def search_data(self, index):
        resp = await self.es.search(index=index, body={'query': {'match_all': {}}}, size=200)
        return resp
