from fastapi import APIRouter

from backend.app.core.config import settings

v1 = APIRouter(prefix=settings.VERSION)

# v1.include_router(auth_router, prefix='/auth', tags=['认证'])
