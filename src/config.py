"""Settings for 'Quazar' application."""
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    MODE: Literal["DEV", "TEST", "PROD"]

    # Database
    DB_HOST: str
    DB_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    DB_HOST_TEST: str
    DB_PORT_TEST: str
    POSTGRES_DB_TEST: str
    POSTGRES_USER_TEST: str
    POSTGRES_PASSWORD_TEST: str

    @property
    def TEST_DATABASE_URL(self):
        return (f"postgresql+asyncpg://{self.POSTGRES_USER_TEST}:{self.POSTGRES_PASSWORD_TEST}@"
                f"{self.DB_HOST_TEST}:{self.DB_PORT_TEST}/{self.POSTGRES_DB_TEST}")

    @property
    def ASYNC_DATABASE_URL(self):
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()
