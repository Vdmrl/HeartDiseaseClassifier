import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    LOG_LEVEL: str

    DB_HOST: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    DB_TEST_HOST: str
    DB_TEST_USER: str
    DB_TEST_PASS: str
    DB_TEST_NAME: str

    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    ACCESS_TOKEN_LIFETIME_SECONDS: int

    # dev
    @property
    def DATABASE_URL_asyncpg(self) -> str:  # async
        # DSN for PostgreSQL using asyncpg
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}/{self.DB_NAME}"

    # test
    @property
    def TEST_DATABASE_URL_asyncpg(self) -> str:  # async
        # DSN for PostgreSQL using asyncpg
        return f"postgresql+asyncpg://{self.DB_TEST_USER}:{self.DB_TEST_PASS}@{self.DB_TEST_HOST}/{self.DB_TEST_NAME}"

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    model_config = SettingsConfigDict()


settings = Settings()
