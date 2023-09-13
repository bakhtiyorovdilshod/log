import os
import re

from dotenv import load_dotenv

from backend.app.core.elastic import ElasticConfig
from backend.app.services.elastic_template import elastic_template_service
from backend.app.utils.logger import logger_config

logger = logger_config(__name__)

load_dotenv()


async def validate_data_elastic(service_id: str, table_name: str, method: str, data: dict):
    templates = await elastic_template_service.get_templates(
        service_id=service_id,
        table_name=table_name,
        method=method
    )
    if len(templates) != 0:
        templates = templates[0].get('templates')
        texts = {
            'text_uz': [template for template in templates if template.get('lang') == 'uz'][0].get('text'),
            'text_ru': [template for template in templates if template.get('lang') == 'ru'][0].get('text'),
        }
        text_ru = texts['text_ru'].format(**data)
        text_uz = texts['text_uz'].format(**data)
        data['text_uz'] = text_uz
        data['text_ru'] = text_ru
        return data

    return {}


async def write_data_elastic(index, body):
    logger.info("Writing data to elastic")
    elastic_config = ElasticConfig(
        host=os.environ.get('ELASTIC_HOST'),
        password=os.environ.get('ELASTIC_USERNAME'),
        username=os.environ.get('ELASTIC_PASSWORD')
    )
    await elastic_config.connect()
    # validated_data = await validate_data_elastic(
    #     service_id='64fffbbce29abc320098e187',
    #     table_name='organization',
    #     method='create',
    #     data=body
    # )
    resp = await elastic_config.save_data(index, body)

