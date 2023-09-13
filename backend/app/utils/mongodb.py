from backend.app.database.mongodb import db
from backend.app.utils.logger import logger_config

logger = logger_config(__name__)


async def get_rabbitmq_template(rabbit_data: dict, queue_name: str):
    table_name = rabbit_data.get('table_name')
    method = rabbit_data.get('method')
    requirement_fields = []
    rabbit_template = await db.db['Indexation_templates'].find_one(
        {
            'queue_name': queue_name,
            'table_name': table_name
        }
    )
    if rabbit_template:
        validations = rabbit_template.get('validation')
        if len(validations) != 0:
            fields = [validation.get('fields', []) for validation in validations if
                                  validation.get('method') == method]
            if len(fields) != 0:
                requirement_fields = fields[0]
    return requirement_fields


async def write_to_mongodb(data, collection):
    logger.info("Writing data to mongodb")
    result = await db.db[collection].insert_one(data)