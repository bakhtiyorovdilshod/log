import uvicorn
from src.core.app import log_app

if __name__ == "__main__":
    uvicorn.run("main:log_app", host="127.0.0.1", port=8090, reload=True)