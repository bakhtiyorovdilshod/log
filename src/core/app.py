import os
from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.database import db
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()


@app.on_event('startup')
async def startup():
    await db.connect_to_database(path=os.environ.get('MongoDB_URL'))


@app.on_event("shutdown")
async def shutdown():
    await db.close_database_connection()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/items/")
async def create_item(item: Dict):
    result = await db.db['log'].insert_one(item)
    return {"id": str(result.inserted_id)}