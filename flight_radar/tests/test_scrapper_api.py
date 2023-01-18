import pytest
import requests_mock

from flight_radar.models.config import ConfigRepo
from flight_radar.repos.scrapper import TequilaAPI
from flight_radar.repos.scrapper_config_handler import ConfigHandler

EXAMPLE_URL = 'https://example.url'


@pytest.fixture
def scrapper_api() -> TequilaAPI:
    scrapper_config: ConfigHandler = ConfigHandler(ConfigRepo)
    return TequilaAPI(scrapper_config)


def test_if_scrapper_is_configured_properly(scrapper_api) -> None:
    """ Test if scrapper repo instance can be created """
    assert isinstance(scrapper_api.config, ConfigHandler)


@pytest.mark.asyncio
async def test_fetch_method(scrapper_api) -> None:
    """ Check if __fetch_data method is available in scrapper repo """
    content = {'Success': 'request ok'}
    with requests_mock.Mocker() as mock_request:
        mock_request.get(EXAMPLE_URL, json=content)
        response = await scrapper_api._TequilaAPI__fetch_data(EXAMPLE_URL, content)  # type: ignore
    assert response == content
