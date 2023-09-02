import motor.motor_asyncio
import logging, os
from pymongo import MongoClient
from pymongo.database import Database

import motor.motor_asyncio
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
import motor


MONGO_DETAILS = os.environ.get('MONGO_URL',' mongodb://localhost:27017')

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.hr_log

state_collection = database.get_collection('state_collection')


class MongoManager:
    client: MongoClient = None
    db: Database = None

    def connect_to_database(self, path: str):
        print("Connecting to MongoDB.")
        self.client = MongoClient(path)
        self.db = self.client['hr_log']
        print("Connected to MongoDB.")

    def close_database_connection(self):
        logging.info("Closing connection with MongoDB.")
        self.client.close()
        logging.info("Closed connection with MongoDB.")


mongo_manager = MongoManager()
