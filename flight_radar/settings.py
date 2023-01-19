import logging
from datetime import datetime


def get_module_logger(mod_name) -> logging:
    """
    To use this, do logger = get_module_logger(__name__)
    """
    logger: logging = logging.getLogger(mod_name)
    stream_handler: logging = logging.StreamHandler()
    log_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep + os.pardir), "logs")
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
DATABASES: dict = {
    "default": {
        "NAME": "",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    }
}

try:
    from _local_settings import *
except Exception as e:
    print(f"No local settings. {e}")
