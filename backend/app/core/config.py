from typing import Any, Dict, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "AgroIntel AI Platform"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Security
    SECRET_KEY: str = "changeme-for-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # PostgreSQL config
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "agrointel"
    POSTGRES_PORT: str = "5432"
    DATABASE_URL: Optional[str] = None

    # Ingestion Settings
    OPENWEATHER_API_KEY: Optional[str] = None
    NASA_POWER_API_KEY: Optional[str] = None
    WEATHER_POLLING_INTERVAL_MINUTES: int = 60
    HTTP_TIMEOUT_SECONDS: float = 10.0

    # Processing Settings
    PROCESSING_INTERVAL_MINUTES: int = 60  # Should typically run after ingestion

    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return f"postgresql+asyncpg://{values.get('POSTGRES_USER')}:{values.get('POSTGRES_PASSWORD')}@{values.get('POSTGRES_SERVER')}:{values.get('POSTGRES_PORT')}/{values.get('POSTGRES_DB')}"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()
