from pydantic import BaseModel, Field
from typing import Optional, List


class OauthLogConsumerSchemaChildren(BaseModel):
    time: Optional[str]


class OauthLogConsumerSchema(BaseModel):
    method: Optional[str]
    table_name: Optional[str]
    user_id: Optional[int]
    data: List[OauthLogConsumerSchemaChildren]