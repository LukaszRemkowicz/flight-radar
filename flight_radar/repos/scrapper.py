import logging
import urllib.parse
from dataclasses import dataclass
from typing import Optional, Type

from aiohttp import ClientResponse as Response

from logger import get_module_logger
from models.entities import TequilaFlightList
from models.types import TequilaUrls
from repos.adapters import (
    TenacityAdapter as tenacity,
)
from repos.interfaces import TequilaSessionAdapterProtocol
from settings import settings
from utils.mock_response_object_for_debug_mode import save_response

logger: logging.Logger = get_module_logger(__name__)


@dataclass
class TequilaAPI:
    """Tequila API scrapper"""

    session_adapter: TequilaSessionAdapterProtocol
    urls: Type[TequilaUrls] = TequilaUrls

    # @tenacity.retry(settings.get_tenacity_config())
    async def fetch(self, url: str, **kwargs) -> Optional[dict]:
        """
        Fetch data with given url and kwargs using GET method,
        using tenacity object
        """
        logger.info(f"Started parsing {url + urllib.parse.urlencode(kwargs)}")
        response: Response = await self.session_adapter.session.get(
            url=url, params=kwargs
        )
        data = await response.json()

        if data.get("status") == "Bad Request":
            raise Exception(data.get("error"))

        response.raise_for_status()
        logger.info("Success")

        return data

    async def get_flight(self, kwargs: dict) -> Optional[TequilaFlightList]:
        """Get flight data with given search params"""
        result: dict = await self.fetch(self.urls.FLIGHT_SEARCH, **kwargs)
        if settings.DEBUG:
            await save_response(result)
        if result:
            flights: TequilaFlightList = TequilaFlightList(
                search_id=result.get("search_id"), flights=result.get("data")
            )
            return flights
        return None

    async def get_destination_code(self, city_name: str) -> str:
        """Get destination code for given city name"""
        query = {"term": city_name, "location_types": "city"}
        response = await self.fetch(url=self.urls.FIND_LOCATION, **query)

        results = response["locations"]
        code = results[0]["code"]
        return code
