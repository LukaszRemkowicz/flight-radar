import os
from dataclasses import dataclass
from enum import Enum, IntEnum

from dotenv import find_dotenv, load_dotenv
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from models.types import Config

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

env_path: str = os.path.join(ROOT_PATH, ".env")
load_dotenv(env_path)


MAX_WAIT_BEFORE: int = 2
MIN_WAIT_BEFORE: int = 2


class DatabaseSettings(BaseSettings):
    """Database settings"""

    host: str = "localhost"
    port: int = 5432
    username: str = "postgres"
    password: SecretStr = SecretStr("postgres")
    name: str = "postgres"


class Settings(BaseSettings):
    DEBUG: bool = False
    TEQUILA_API_KEY: str = ""
    db: DatabaseSettings
    MIN_WAIT_BEFORE: int = 2
    MAX_WAIT_BEFORE: int = 2
    MAX_ATTEMPTS: int = 4
    MIN_WAIT_BETWEEN: int = 5
    MAX_WAIT_BETWEEN: int = 5
    model_config = SettingsConfigDict(
        env_file=find_dotenv(),
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="allow",
    )

    def get_tenacity_config(self) -> Config:
        return Config(
            MIN_WAIT_BEFORE=self.MIN_WAIT_BEFORE,
            MAX_WAIT_BEFORE=self.MAX_WAIT_BEFORE,
            MAX_ATTEMPTS=self.MAX_ATTEMPTS,
            MIN_WAIT_BETWEEN=self.MIN_WAIT_BETWEEN,
            MAX_WAIT_BETWEEN=self.MAX_WAIT_BETWEEN,
        )


settings = Settings()


def get_db_credentials() -> dict:
    return {
        "host": settings.db.host,
        "port": settings.db.port,
        "user": settings.db.username,
        "password": settings.db.password.get_secret_value(),
        "database": settings.db.name,
    }


DB_CONFIG: dict = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": get_db_credentials(),
        },
    },
    "apps": {
        "models": {
            "models": ["__main__", "models.models", "aerich.models"],
            "default_connection": "default",
        },
    },
    "default_connection": "default",
}


class MockedUsers(IntEnum):
    ANONYMOUS_USER = 1


try:
    if not os.environ.get("TEST"):
        from _local_settings import *
except Exception as e:
    print(f"No local settings. {e}")
