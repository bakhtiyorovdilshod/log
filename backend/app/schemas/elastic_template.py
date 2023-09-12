from pydantic import BaseModel, Field
from typing import Optional, List


class ElasticTemplateTypeSchema(BaseModel):
    lang: str
    text: str


class ElasticTemplateCreateSchema(BaseModel):
    service_id: str
    table_name: str
    method: str
    templates: List[ElasticTemplateTypeSchema]

    class Config:
        json_schema_extra = {
            'example': {
                'service_id': '64fffbbce29abc320098e187',
                'table_name': 'user',
                'method': 'create',
                'templates': [
                    {
                        'lang': 'uz',
                        'text': '$fullname ${date}da tashkilot nomini $oldName dan ${newName}ga  o\'zgartirdi'
                    },
                    {
                        'lang': 'ru',
                        'text': '$fullname изменил название организации с $oldName на ${newName} ${date}'
                    }
                ]

            }
        }


class ElasticTemplateCreateResponseSchema(BaseModel):
    id: str
    table_name: str
    method: str
    templates: List[ElasticTemplateTypeSchema]

    class Config:
        json_schema_extra = {
            'example': {
                'id': '64fffbbce29abc320098e187',
                'table_name': 'user',
                'method': 'create',
                'templates': [
                    {
                        'lang': 'uz',
                        'text': '$fullname ${date}da tashkilot nomini $oldName dan ${newName}ga  o\'zgartirdi'
                    },
                    {
                        'lang': 'ru',
                        'text': '$fullname изменил название организации с $oldName на ${newName} ${date}'
                    }
                ]

            }
        }


class ErrorResponseSchema(BaseModel):
    error: str
    code: str
    message: str


class ElasticTemplateUpdateSchema(BaseModel):
    table_name: str
    method: str
    templates: List[ElasticTemplateTypeSchema]

    class Config:
        json_schema_extra = {
            'example': {
                'table_name': 'user',
                'method': 'create',
                'templates': [
                    {
                        'lang': 'uz',
                        'text': '$fullname ${date}da tashkilot nomini $oldName dan ${newName}ga  o\'zgartirdi'
                    },
                    {
                        'lang': 'ru',
                        'text': '$fullname изменил название организации с $oldName на ${newName} ${date}'
                    }
                ]

            }
        }


class ElasticTemplateFilterParamsSchema(BaseModel):
    service_id: str
