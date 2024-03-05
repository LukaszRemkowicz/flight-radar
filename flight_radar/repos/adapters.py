from dataclasses import dataclass, field

import requests
from tenacity import (
    stop_after_attempt,
    wait_random,
    before_log,
    retry_if_exception_type,
    after_log,
)
from typing_extensions import Any

from models.types import RequestHeaders, Config
from settings import settings
import json
import logging
from asyncio import sleep
from random import randint
from typing import Coroutine, Optional, Tuple, Callable, Type

import tenacity

from logger import get_module_logger
from models.types import RequestHeaders
from requests import exceptions
from urllib3.exceptions import NewConnectionError
from utils.exceptions import BadRequestException

logger: logging.Logger = get_module_logger(__name__)

import aiohttp


@dataclass
class TequilaSessionAdapter:
    _headers: dict = field(default_factory=RequestHeaders())
    _session: Optional[aiohttp.ClientSession] = None
    tequila_api_key: str = settings.TEQUILA_API_KEY

    @property
    def session(self) -> aiohttp.ClientSession:
        if self._session is None:
            raise RuntimeError(
                "Session is not initialized. Call 'initialize_session' first."
            )
        return self._session

    @property
    def headers(self) -> dict[str, str]:
        return self._headers

    async def initialize_session(self):
        self._session = aiohttp.ClientSession()
        self.prepare_headers()

    def prepare_headers(self):
        self._session.headers.update(self.headers)
        self._session.headers.update({"apikey": self.tequila_api_key})


def error_callback(retry_state: tenacity.RetryCallState) -> Optional[Tuple]:
    """Error callback for tenacity retrying"""
    state: HTTPError = retry_state.outcome._exception  # noqa
    if state.response.status_code == 400:
        response = json.loads(state.response.__dict__["_content"].decode("utf-8"))
        raise BadRequestException(f'{response.get("status")}: {response.get("error")}')
    return (lambda err_state: logger.info(err_state.outcome.exception()))(retry_state)


class TenacityAdapter:
    """
    A utility class providing a decorator to apply tenacity retries to functions.

    This adapter enables the application of tenacity retries to functions by using
    a decorator, allowing customized retry settings to be optionally provided.

    Usage:
    - Apply the `retry` decorator to the desired function, specifying optional
    `config` settings.
    - The `config` parameter allows dynamic configuration of retry settings.

    Example:
    ```
    tenacity_adapter = TenacityAdapter()

    @tenacity_adapter.retry(config=my_config)
    def my_function():
        pass
    ```

    Args:
    - config (Optional[Config]): Optional configuration settings for retries.

    Returns:
    - decorator: A decorator function to apply tenacity retries to a target function.
    """

    @staticmethod
    def retry(
        config: Optional[Config] = None,
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """
        Decorator function to apply tenacity retries to a target function.

        Args:
        - config (Optional[Config]): Optional configuration settings for retries.

        Returns:
        - decorator: A decorator function to apply tenacity retries to a target function.
        """

        def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
            retry_settings: Config = config

            @tenacity.retry(
                stop=stop_after_attempt(retry_settings.MAX_ATTEMPTS or 3),
                wait=wait_random(settings.MIN_WAIT_BETWEEN, settings.MAX_WAIT_BETWEEN),
                before=before_log(logger, logging.INFO),
                retry=tenacity.retry_if_not_exception_type(
                    (exceptions.ConnectionError, NewConnectionError)
                ),
                after=tenacity.after_log(logger, logging.INFO),
                retry_error_callback=error_callback,
            )
            def wrapper(*args, **kwargs) -> Any:
                return fn(*args, **kwargs)

            return wrapper

        return decorator
