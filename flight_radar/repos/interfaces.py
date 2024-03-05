from dataclasses import dataclass
from typing import Protocol, Optional

import aiohttp

from models.entities import TequilaFlightList


class ScrapperProtocol(Protocol):
    async def fetch(self, url: str, **kwargs) -> Optional[dict]:
        ...

    async def get_flight(self, kwargs: dict) -> Optional[TequilaFlightList]:
        ...

    async def get_destination_code(self, city_name: str) -> str:
        ...


class TequilaSessionAdapterProtocol(Protocol):
    def prepare_headers(self) -> None:
        ...

    @property
    def session(self) -> aiohttp.ClientSession:  # noqa
        ...

    @property
    def headers(self) -> dict[str, str]:  # noqa
        ...

    async def initialize_session(self) -> None:
        ...
