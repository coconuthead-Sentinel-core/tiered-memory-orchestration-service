import os
from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- Core Application ---
    PROJECT_NAME: str = "Sovereign Forge"
    VERSION: str = "4.0.0"
    ENVIRONMENT: str = "development"  # development, production
    LOG_LEVEL: str = "INFO"
    API_KEY: str = "secret"

    # --- AI Provider ---
    AOAI_ENDPOINT: str = ""
    AOAI_KEY: str = ""  # Mapped from API_KEY in .env if needed, or separate
    AOAI_CHAT_DEPLOYMENT: str = "gpt-4"
    AOAI_EMBED_DEPLOYMENT: str = "text-embedding-ada-002"
    AOAI_API_VERSION: str = "2024-08-01-preview"
    MOCK_AI: bool = False

    # --- Infrastructure (Cosmos DB) ---
    COSMOS_ENDPOINT: str = "https://localhost:8081/"
    COSMOS_KEY: str = ""
    COSMOS_DATABASE_NAME: str = "SentinelForgeDB"
    COSMOS_CONTAINER_NAME: str = "Items"

    # --- Performance ---
    RATE_LIMIT_QPS: float = 10.0

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
