import pytest
import requests_mock

from repos.scrapper_config_handler import ConfigHandler
from models.entities import FlightsListIn
from models.types import UrlConfigs

EXAMPLE_URL = "https://example.url"


def test_if_scrapper_is_configured_properly(scrapper_api) -> None:
    """Test if scrapper repo instance can be created"""
    assert isinstance(scrapper_api.config, ConfigHandler)


@pytest.mark.asyncio
async def test_fetch_method(scrapper_api) -> None:
    """Check if __fetch_data method is available in scrapper repo"""
    content: dict = {"Success": "request ok"}
    with requests_mock.Mocker() as mock_request:
        mock_request.get(EXAMPLE_URL, json=content)
        response = await scrapper_api._TequilaAPI__fetch_data(EXAMPLE_URL, content)  # type: ignore
    assert response == content


@pytest.mark.asyncio
async def test_get_flights(flight_params, load_response_data, scrapper_api) -> None:
    """Test if valid flight data is returned"""
    with requests_mock.Mocker() as mock_request:
        mock_request.get(UrlConfigs.TEQUILA_URL, json=load_response_data)
        response: FlightsListIn = await scrapper_api.get_flight(flight_params)
    assert isinstance(response, FlightsListIn)
    assert isinstance(response.flights, list)
