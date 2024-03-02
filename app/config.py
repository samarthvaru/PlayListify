import os
from pathlib import Path
from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings

os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = "1"

class Settings(BaseSettings):
    base_dir: Path = Path(__file__).resolve().parent
    templates_dir: Path = Path(__file__).resolve().parent / "templates"
    astradb_keyspace: str 
    astradb_client_id: str
    astradb_client_secret: str
    secret_key: str
    jwt_algorithm: str = Field(default='HS256')
    session_duration: int = Field(default=86400)

    class Config:
        env_file = '.env'
        extra = 'allow'

@lru_cache(maxsize=None)
def get_settings():
    return Settings()