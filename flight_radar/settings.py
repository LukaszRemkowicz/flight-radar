import logging
from datetime import datetime


def get_module_logger(mod_name):
    """
    To use this, do logger = get_module_logger(__name__)
    """
    logger = logging.getLogger(mod_name)
    stream_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(f"{datetime.now().date()}.log")

    formatter = logging.Formatter(
        "%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s"
    )
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    logger.addHandler(logging.FileHandler(f"{datetime.now().date()}.log"))
    logger.setLevel(logging.INFO)
    return logger


MAX_WAIT_BEFORE = 2
MIN_WAIT_BEFORE = 2

TEQUILLA_API_KEY = ""
DATABASES = {
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
