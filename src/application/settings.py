from datetime import timedelta

from pydantic import AnyHttpUrl, PostgresDsn
from pydantic_settings import BaseSettings


class PostgresSettings(BaseSettings):
    SCHEMA_NAME: str | None = "main"

    POSTGRES_NAME: str | None = "postgres"
    POSTGRES_USER: str | None = "postgres"
    POSTGRES_PASSWORD: str | None = "postgres"
    POSTGRES_SERVER: str | None = "hook-db"
    POSTGRES_PORT: int | None = 5432

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_SERVER}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_NAME or ''}"
        )


class Settings(PostgresSettings):
    API_V1_STR: str = "/api"
    BACKEND_TOKEN_EXP: int | None = 86400
    TESTING: bool | None = False

    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    @property
    def TOKEN_EXP(self) -> timedelta:
        return timedelta(seconds=self.BACKEND_TOKEN_EXP)


settings: Settings = Settings()

NUMBERS_WEIGHT = {1: 20, 2: 100, 3: 45, 4: 70, 5: 15, 6: 140, 7: 20, 8: 20, 9: 140, 10: 45}
