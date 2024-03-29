import os
from pathlib import Path
from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings

os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = "1"

class Settings(BaseSettings):
    
    """
    Settings class for managing application settings.

    Attributes:
    - base_dir: Base directory path for the application.
    - templates_dir: Directory path for the application templates.
    - astradb_keyspace: Keyspace for the Cassandra database.
    - astradb_client_id: Client ID for the Cassandra database.
    - astradb_client_secret: Client secret for the Cassandra database.
    - secret_key: Secret key for the application.
    - jwt_algorithm: Algorithm used for JWT token generation.
    - session_duration: Duration of a session in seconds.
    - algolia_app_id: App ID for Algolia search indexing.
    - algolia_api_key: API key for Algolia search indexing.
    - algolia_index_name: Name of the index in Algolia.

    Config:
    - env_file: Name of the environment file.
    - extra: How to handle extra fields ('allow' allows extra fields).
    """
    
    base_dir: Path = Path(__file__).resolve().parent
    templates_dir: Path = Path(__file__).resolve().parent / "templates"
    astradb_keyspace: str 
    astradb_client_id: str
    astradb_client_secret: str
    secret_key: str
    jwt_algorithm: str = Field(default='HS256')
    session_duration: int = Field(default=86400)
    algolia_app_id: str
    algolia_api_key: str
    algolia_index_name: str


    class Config:
        env_file = '.env'
        extra = 'allow'

@lru_cache(maxsize=None)
def get_settings():
    return Settings()