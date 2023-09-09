from pydantic import BaseModel, Field
from typing import Optional, List
from backend.app.database.mongodb import db
from pydantic import validator


class RabbitMQTemplateBase(BaseModel):
    """rabbitmq template """

    name: str


class RabbitMQTemplateById(BaseModel):
    id: str


