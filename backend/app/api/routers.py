from fastapi import APIRouter

from backend.app.core.config import settings
from backend.app.api.v1.rabbitmq_template import rabbit_template_router
from backend.app.api.v1.rabbitmq_template import service_router
from backend.app.api.v1.elastic_template import router as elastic_template_router
from backend.app.api.v1.elastic_result import router as elastic_result_router

v1 = APIRouter(prefix='')


v1.include_router(rabbit_template_router, prefix="/rabbit_template", tags=['rabbit'])
v1.include_router(service_router, prefix="/service", tags=['service-type'])
v1.include_router(elastic_template_router, prefix="/elastic_template", tags=['elastic-template'])
v1.include_router(elastic_result_router, prefix="/elastic_result", tags=['elastic-result'])
