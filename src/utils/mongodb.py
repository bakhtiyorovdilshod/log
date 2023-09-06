
from src.core.database import db
from src.utils.logger import logger_config

logger = logger_config(__name__)


async def write_to_mongodb(data, collection):
    logger.info("Writing data to mongodb")
    result = await db.db[collection].insert_one(data)