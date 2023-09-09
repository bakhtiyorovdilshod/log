from pydantic import BaseModel, Field
from typing import Optional, List
from backend.app.database.mongodb import db
from pydantic import validator


class RabbitMQTemplateBase(BaseModel):
    """rabbitmq template """

    name: str


class RabbitMQTemplateById(BaseModel):
    id: str


class RabbitConsumerFieldsBase(BaseModel):
    key: str
    type: str


class RabbitConsumerValidationBase(BaseModel):
    method: str
    fields: set[list] = [RabbitConsumerFieldsBase]


class RabbitConsumerBase(BaseModel):
    queue_name: str
    table_name: str
    validation: set[list] = RabbitConsumerValidationBase
