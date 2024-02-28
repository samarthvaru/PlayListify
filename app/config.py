import os
from functools import lru_cache
from pydantic_settings import BaseSettings

os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = "1"

class Settings(BaseSettings):
    astradb_keyspace: str 
    astradb_client_id: str
    astradb_client_secret: str

    class Config:
        env_file = '.env'
        extra = 'allow'

@lru_cache(maxsize=None)
def get_settings():
    return Settings()