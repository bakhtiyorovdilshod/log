import os
from fastapi import APIRouter, Query
from fastapi.encoders import jsonable_encoder
from dotenv import load_dotenv
from backend.app.core.elastic import ElasticConfig
from backend.app.utils.elastic import validate_data_elastic

load_dotenv()

router = APIRouter()


@router.get(
    "/",
    response_description='searching data',
)
async def elastic_search():
    elastic_config = ElasticConfig(
        host=os.environ.get('ELASTIC_HOST'),
        password=os.environ.get('ELASTIC_USERNAME'),
        username=os.environ.get('ELASTIC_PASSWORD')
    )
    await elastic_config.connect()
    resp = await elastic_config.search_data('index-oauth')
    return resp


@router.get(
    "/elastic_validate",
    response_description='searching data',
)
async def elastic_validate():
    x = await validate_data_elastic(
        service_id='64fffbbce29abc320098e187',
        table_name='organization',
        method='create',
        data={'table_name': 'organization', 'method': 'create', 'fullname': 'Dilshod', 'date': '2022-01-01', 'oldName': 'Umid', 'newName': 'Moliya'}
    )
    return x