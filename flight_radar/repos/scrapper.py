import json
import logging
from typing import Optional

import requests
from requests import Response

from models.pydantic_validators import FlightsListIn
from models.types import UrlConfigs
from repos.scrapper_config_handler import ConfigHandler
from settings import get_module_logger, TEQUILA_API_KEY

logger: logging.Logger = get_module_logger("scrapper")


class TequilaAPI:
    def __init__(self, config: ConfigHandler) -> None:
        self.config: ConfigHandler = config
        self.urls: UrlConfigs = UrlConfigs()
        self.session: requests.Session = requests.Session()

    async def __fetch_data(self, url: str, kwargs: dict):
        """requests method"""

        async def fetch():
            self.session.headers.update(self.config.headers())
            self.session.headers.update({"apikey": TEQUILA_API_KEY})
            logger.info(f"Started parsing {url}")
            response: Response = self.session.get(url=url, params=kwargs)
            response.raise_for_status()
            logger.info("Success")
            return response.json()

        return await (await self.config.tenacity(fetch))()

    async def get_flight(self, kwargs: dict) -> Optional[FlightsListIn]:
        """Get flight data with given params"""
        result: dict = await self.__fetch_data(self.urls.TEQUILA_URL, kwargs)
        if result:
            flights: FlightsListIn = FlightsListIn(flights=result.get("data"))
            return flights
        return None
