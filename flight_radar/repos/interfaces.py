from typing import Protocol, Optional, Callable

import aiohttp
import tenacity

from models.entities import TequilaFlightList
from models.types import Config


class TenacityAdapterProtocol(Protocol):
    def __init__(self, config: Config):
        ...

    async def sleep(self) -> None:
        ...

    async def tenacity(self, fn: Callable) -> tenacity:
        ...


class TequilaSessionAdapterProtocol(Protocol):
    def __init__(self):
        ...

    def prepare_headers(self) -> None:
        ...

    @property
    def session(self) -> aiohttp.ClientSession:
        """"""

    @property
    def headers(self) -> dict[str, str]:
        """"""

    async def initialize_session(self) -> None:
        ...