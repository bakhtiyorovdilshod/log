import aiohttp
from datetime import datetime
from elasticsearch import Elasticsearch
import asyncio
from .config import es_auth
from fastapi import APIRouter, Depends, HTTPException, Query

es = Elasticsearch("http://localhost:9200")


async def main():
    resp = await es.search(
        index="documents",
        query={"match": {}},
        size=20
    )


async def startup():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


async def app_shutdown():
    await es.close()


def get_es_client():
    es_client = Elasticsearch(es_auth.host, basic_auth=(es_auth.user, es_auth.password.get_secret_value()))

    try:
        yield es_client
    finally:
        es_client.close()


class BaseElasticSearch:
    """Elasticsearch saving, searching"""

    async def search(self, query: str = Query(alias='search ...'), es_client: ElasticSearch = Depends(get_es_client, ),
                     index_name: str | None = None, field: str | None = None):
        """searching ..."""

        if len(query.strip()) == 0:
            raise HTTPException(status_code=400, detail="please provide valid query")
        search_query = {
            "query": {
                "match": {
                    field: query
                }
            }
        }
        result = es_client.search(index=index_name, body=search_query)['hits']['hits']
        return result

    async def create_elastic(self, index_name, data):
        """ElasticSearch create """

        result_elastic = es.index(index=index_name, body=data)
        return result_elastic

    async def get_all_index(self, index_name):
        """get all indexing data from Elasticsearch"""

        response = es.get(index=index_name, size=100)['hits']['hits']
        return response

    async def get_index(self, index_name, ObjectId):
        """get one index data by ObjectId"""

        response = es.get(index=index_name, id=ObjectId)['hits']['hits']
        return response

