import os
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from backend.app.utils.logger import logger_config

logger = logger_config(__name__)


class MongoManager:
    """
        MongoManager for connecting and disconnecting database
    """

    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    # database connect and close connections
    async def connect_to_database(self, path: str):
        logger.info("Connecting to MongoDB")
        self.client = AsyncIOMotorClient(path, maxPoolSize=10, minPoolSize=10)
        self.db = self.client['dev_log']

        logger.info(
            "Connected to MongoDB -  %s environment!", os.getenv("ENVIRONMENT", "DEV")
        )

    async def close_database_connection(self):
        logger.info("Closing connection to MongoDB")
        self.client.close()
        logger.info("MongoDB connection closed")

    async def get_collection_data(self, collection):
        mongodb_collection = self.db[collection]
        mongo_data = await mongodb_collection.find({}).to_list(None)
        return mongo_data


db = MongoManager()