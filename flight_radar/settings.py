import logging
from datetime import datetime
import os

from dotenv import load_dotenv


ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

env_path: str = os.path.join(ROOT_PATH, ".env")
load_dotenv(env_path)


def get_module_logger(mod_name) -> logging:
    """
    To use this, do logger = get_module_logger(__name__)
    """
    logger: logging = logging.getLogger(mod_name)
    stream_handler: logging = logging.StreamHandler()
    log_dir = os.path.join(ROOT_PATH + os.sep + os.pardir, "logs")

    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    file_handler: logging = logging.FileHandler(
        f"{log_dir}/{datetime.now().date()}.log"
    )

    formatter: logging = logging.Formatter(
        "%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s"
    )
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    logger.addHandler(logging.FileHandler(f"{log_dir}/{datetime.now().date()}.log"))
    logger.setLevel(logging.INFO)
    return logger


MAX_WAIT_BEFORE: int = 2
MIN_WAIT_BEFORE: int = 2

TEQUILA_API_KEY: str = ""


def get_db_credentials() -> dict:
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": os.getenv("DB_PORT", 5432),
        "user": os.getenv("DB_USERNAME", "postgres"),
        "password": os.getenv("DB_PASSWORD", "postgres"),
        "database": os.getenv("DB_NAME", "postgres"),
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

try:
    if not os.environ.get("TEST"):
        from _local_settings import *
except Exception as e:
    print(f"No local settings. {e}")
