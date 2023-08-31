import os
from pydantic_settings import BaseSettings

from dotenv import load_dotenv
load_dotenv()


class Config(BaseSettings):
    PROJECT_NAME: str = 'logs'
    VERSION: str = '1.0.0'
    MongoDB_URL: str = os.environ.get('MongoDB_URL')


settings = Config()