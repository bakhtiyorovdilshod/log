from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from src.oauth_log.schemas.log import response_model
from src.oauth_log.services.log import oauth_log_service


router = APIRouter()


@router.get(
    "/logs/",
    response_description="log list"
)
async def get_logs():
    logs = await oauth_log_service.logs()
    if logs:
        return response_model(logs, "Logs data retrieved successfully")
    return response_model(logs, "Empty list returned")