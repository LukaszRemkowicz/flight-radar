import json
import logging
from asyncio import sleep
from random import randint
from typing import List

import tenacity
from requests import exceptions
from urllib3.exceptions import NewConnectionError

from utils.exceptions import BadRequestException
from utils.scrapper_config import ConfigRepo
from models.types import RequestHeaders, Config
from settings import get_module_logger

logger: logging.Logger = get_module_logger("scrapper_cfg")


def error_callback(retry_state: tenacity.RetryCallState):
    state: HTTPError = retry_state.outcome._exception  # noqa
    if state.response.status_code == 400:
        response = json.loads(state.response.__dict__["_content"].decode("utf-8"))
        breakpoint()
        raise BadRequestException(f'{response.get("status")}: {response.get("error")}')
    return (lambda err_state: logger.info(err_state.outcome.exception()))(retry_state)


class ConfigHandler:
    """Configurator that supply our scrapper with endpoints, utils and headers"""

    headers: RequestHeaders = RequestHeaders()
    __config_repo: ConfigRepo
    config: ConfigRepo

    updated = False

    def __init__(self, repo):
        self.__config_repo = repo()

    async def sleep(self):
        """
        delay between requests
        """
        if not self.updated:
            await self.get_tenacity_config()
        return await sleep(
            randint(
                self.config.MIN_WAIT_BEFORE,
                self.config.MAX_WAIT_BEFORE,
            )
        )

    async def get_tenacity_config(self):
        self.config = await self.__config_repo.get_config()
        self.updated = True

    async def tenacity(self, fn):
        if not self.updated:
            await self.get_tenacity_config()
        await self.sleep()
        return tenacity.retry(
            stop=tenacity.stop_after_attempt(self.config.MAX_ATTEMPTS),
            wait=tenacity.wait_random(
                self.config.MIN_WAIT_BETWEEN,
                self.config.MAX_WAIT_BETWEEN,
            ),
            before=tenacity.before_log(logger, logging.INFO),
            retry=tenacity.retry_if_not_exception_type(
                (exceptions.ConnectionError, NewConnectionError)
            ),
            after=tenacity.after_log(logger, logging.INFO),
            retry_error_callback=error_callback,
        )(fn)
