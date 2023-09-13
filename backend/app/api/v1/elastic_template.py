from fastapi import APIRouter, Query
from fastapi.encoders import jsonable_encoder

from backend.app.schemas.elastic_template import ElasticTemplateCreateSchema, ElasticTemplateCreateResponseSchema, \
    ErrorResponseSchema, ElasticTemplateUpdateSchema, ElasticTemplateFilterParamsSchema
from backend.app.services.elastic_template import elastic_template_service

router = APIRouter()


@router.post(
    "/",
    response_description='Adding Elastic Template',
)
async def create_elastic_template(data: ElasticTemplateCreateSchema) -> dict:
    data = jsonable_encoder(data)
    response = await elastic_template_service.create_template(data)
    return response


@router.put(
    "/{id}/",
    response_description='Update Elastic Template',
)
async def update_elastic_template(id: str, data: ElasticTemplateUpdateSchema) -> dict:
    data = jsonable_encoder(data)
    response = await elastic_template_service.update_template(id, data)
    return response


@router.get(
    "/{id}/",
    response_description='Get Detail of Elastic Template',
)
async def detail_elastic_template(id: str) -> dict:
    response = await elastic_template_service.detail_template(id)
    return response


@router.get(
    "/",
    response_description='Get List of Elastic Templates',
)
async def list_elastic_template(service_id: str = None):
    response = await elastic_template_service.list_templates(service_id)
    return response



