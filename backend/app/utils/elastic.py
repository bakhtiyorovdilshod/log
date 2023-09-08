import os

from dotenv import load_dotenv

from backend.app.core.elastic import ElasticConfig
from backend.app.utils.logger import logger_config

logger = logger_config(__name__)

load_dotenv()


async def write_data_elastic(index, body):
    logger.info("Writing data to elastic")
    elastic_config = ElasticConfig(
        host=os.environ.get('ELASTIC_HOST'),
        password=os.environ.get('ELASTIC_USERNAME'),
        username=os.environ.get('ELASTIC_PASSWORD')
    )
    await elastic_config.connect()
    resp = await elastic_config.save_data(index, body)

