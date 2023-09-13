from backend.app.database.mongodb import db
from backend.app.services.rabbit_service_template import RabbitServiceTemplate
from backend.app.utils.elastic import write_data_elastic
from backend.app.utils.logger import logger_config
from backend.app.utils.rabbit import validate_rabbitmq_data

logger = logger_config(__name__)


async def write_to_mongodb_and_elastic(queue_name: str, rabbit_data: dict, collection: str, index_elastic: str):
    logger.info("Writing data to mongodb")
    rabbit_template = RabbitServiceTemplate()
    requirements = await rabbit_template.get_rabbitmq_template(
        queue_name=queue_name,
        table_name=rabbit_data.get('table_name'),
        method=rabbit_data.get('method')
    )
    elastic_data = rabbit_data
    status = await validate_rabbitmq_data(rabbit_data, requirements)
    if status:
        result = await db.db[collection].insert_one(rabbit_data)
        await write_data_elastic(index_elastic, elastic_data)