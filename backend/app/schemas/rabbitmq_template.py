from pydantic import BaseModel, Field
from typing import Optional, List
from backend.app.database.mongodb import db
from pydantic import validator
from typing import Tuple
from typing import List
from fastapi import Depends, FastAPI, Query


class RabbitMQTemplateBase(BaseModel):
    """rabbitmq template """

    name: str


class RabbitMQTemplateById(BaseModel):
    id: str


# --------------------------------------------   RabbitMQ Consumer -------------------------------------#


class RabbitConsumerFields(BaseModel):
    key: str
    type: str


class RabbitConsumerValidationBase(BaseModel):
    method: str
    fields: List[RabbitConsumerFields]


class RabbitConsumerBase(BaseModel):
    queue_name: str = Query(..., description="queue name")
    table_name: str
    validation: List[RabbitConsumerValidationBase]
