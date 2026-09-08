"""
Application configuration.

All backend configuration is read from environment variables so that the
same Docker image can be reused for different stores/environments without
changing code (see IMPLEMENTATION_PLAN.md, section 31 - Environment Variables).

Never hardcode secrets here. Add new settings as new features need them.
"""

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- App ---
    PROJECT_NAME: str = "Customizable E-Commerce Platform"
    API_V1_PREFIX: str = "/api/v1"
    ENVIRONMENT: str = "development"

    # --- Database ---
    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@db:5432/ecommerce"

    # --- Auth / JWT ---
    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # --- CORS ---
    # Comma-separated list of allowed origins, e.g. "http://localhost:3000,https://mystore.com"
    CORS_ORIGINS: str = "http://localhost:3000"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance - env vars are read once per process."""
    return Settings()


settings = get_settings()
