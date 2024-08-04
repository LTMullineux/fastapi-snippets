from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    # project settings
    VERSION: str = Field("0.0.1")
    PROJECT_NAME: str = Field("Ultimate FastAPI Project Setup")

    # postgres settings
    POSTGRES_DRIVERNAME: str = "postgresql"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int | str = "5432"
    POSTGRES_ECHO: bool = False
    POSTGRES_POOL_SIZE: int = 5


settings = Settings()
