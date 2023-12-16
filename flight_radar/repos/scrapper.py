import logging
import urllib.parse
from typing import Optional, Type

import requests
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


class TequilaAPI:
    """Tequila API scrapper"""

    def __init__(
        self,
        session_adapter: TequilaSessionAdapterProtocol,
        urls: Type[TequilaUrls] = TequilaUrls,
    ) -> None:
        self.urls: Type[TequilaUrls] = urls
        self.session_adapter: TequilaSessionAdapterProtocol = session_adapter

    @tenacity.retry(settings.get_tenacity_config())
    async def fetch(self, url: str, **kwargs) -> dict:
        """
        Fetch data with given url and kwargs using GET method,
        using tenacity object
        """

        """Fetch data"""
        logger.info(f"Started parsing {url + urllib.parse.urlencode(kwargs)}")
        response: Response = await self.session_adapter.session.get(
            url=url, params=kwargs
        )
        data = await response.json()

        if data.get('status') == "Bad Request":
            raise Exception(data.get('error'))

        response.raise_for_status()
        logger.info("Success")

        return data

    # async def get_google(self):
    #     """Get google"""
    #     base_url = "https://fakestoreapi.com/products/"
    #     num_urls = 10  # Number of URLs you want to generate
    #
    #     # Using lambda function with a list comprehension
    #     generate_urls = lambda base, n: [base + str(i) for i in range(1, n + 1)]
    #
    #     list_of_urls = generate_urls(base_url, num_urls)
    #     for url in list_of_urls:
    #         result: dict = await self.__fetch_data(url, {})
    #         print(result)
    #         # return result

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

    async def get_destination_code(self, city_name):
        """Get destination code for given city name"""
        query = {"term": city_name, "location_types": "city"}
        response = await self.fetch(url=self.urls.FIND_LOCATION, **query)

        results = response["locations"]
        code = results[0]["code"]
        return code
