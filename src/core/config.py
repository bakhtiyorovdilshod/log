import os
import secrets
import databases
import sqlalchemy
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    PROJECT_NAME: str = 'hr logs'
    VERSION: str = '1.0.0'


settings = Config()

