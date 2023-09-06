import asyncio

import uvicorn
from src.core.app import app

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=7071, reload=True)