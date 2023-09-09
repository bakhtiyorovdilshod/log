from fastapi import APIRouter

from backend.app.core.config import settings
from backend.app.api.v1.rabbitmq_template import app as rabbit_template_router

v1 = APIRouter(prefix='/api/v1')


v1.include_router(rabbit_template_router, prefix="/rabbit_template", tags=['rabbit-template'])
