import motor.motor_asyncio

MONGO_DETAILS = 'mongodb://localhost:27017'

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.hr_log

state_collection = database.get_collection('state_collection')