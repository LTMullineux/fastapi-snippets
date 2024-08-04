from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    # project
    VERSION: str = Field("0.0.1")
    PROJECT_NAME: str = Field("FastAPI + SQLAlchemy Tile Server")
    SNIPPETS_PORT: int = 8000
    SNIPPETS_HOST: str = "0.0.0.0"

    # postgres
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_ECHO: bool = False
    POSTGRES_POOL_SIZE: int = 5

    # keys
    MAPBOX_ACCESS_TOKEN: str = "YOUR_MAPBOX_ACCESS_TOKEN"


config = Config()
