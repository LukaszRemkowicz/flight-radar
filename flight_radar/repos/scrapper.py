import logging

import requests
from requests import Response

from models.types import UrlConfigs
from repos.scrapper_config_handler import ConfigHandler
from settings import get_module_logger, TEQUILLA_API_KEY

logger: logging.Logger = get_module_logger("scrapper")


class TequilaAPI:
    def __init__(self, config: ConfigHandler) -> None:
        self.config: ConfigHandler = config
        self.urls: UrlConfigs = UrlConfigs()
        self.session: requests.Session = requests.Session()

    async def __fetch_data(
        self, url: str, kwargs: dict
    ):
        """
        method that making requests
        """

        async def fetch():
            self.session.headers.update(self.config.headers())
            self.session.headers.update({'apikey': TEQUILLA_API_KEY})
            logger.info(f"Started parsing {url}")
            response: Response = self.session.get(url=url, params=kwargs)
            response.raise_for_status()

            if response.status_code != 200:
                return 'error'

            logger.info("Success")
            return response.json()

        return await (await self.config.tenacity(fetch))()

    async def get_flight(self, kwargs):
        return await self.__fetch_data('https://api.tequila.kiwi.com/v2/search?', kwargs)
