import logging
import os
from datetime import datetime

from settings import ROOT_PATH


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    green = "\x1b[32;20m"
    reset = "\x1b[0m"
    format = "%(asctime)s - [%(name)-12s] - %(levelname)-8s - %(message)s (%(filename)s:%(lineno)d)"  # noqa: E501

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


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

    formatter = CustomFormatter()
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    logger.addHandler(logging.FileHandler(f"{log_dir}/{datetime.now().date()}.log"))
    logger.setLevel(logging.INFO)
    return logger
