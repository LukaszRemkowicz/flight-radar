import json
import logging
import os
import sys
from typing import TYPE_CHECKING

import requests

import flight_radar.settings as settings
import pytest
from pytest_mock import MockerFixture


if TYPE_CHECKING:
    from pytest_docker.plugin import Services

root_dir = settings.ROOT_PATH
sys.path.append(root_dir)

from utils.scrapper_config import ConfigRepo
from utils.exceptions import TestDBWrongCredentialsError
from models.entities import FlightOut
from repos.scrapper import TequilaAPI
from repos.scrapper_config_handler import ConfigHandler

from dotenv import dotenv_values

env_path: str = os.path.join(settings.ROOT_PATH, ".env")
env_values = dict(dotenv_values(env_path))

TEST_DB_PASSWORD = env_values.get("POSTGRES_TEST_PASSWORD") or os.getenv(
    "POSTGRES_TEST_PASSWORD"
)
TEST_DB_USER = env_values.get("POSTGRES_TEST_USER") or os.getenv("POSTGRES_TEST_USER")
TEST_DB_NAME = env_values.get("POSTGRES_TEST_DB_NAME") or os.getenv(
    "POSTGRES_TEST_DB_NAME"
)


@pytest.fixture(autouse=True)
def disable_network_calls(monkeypatch):
    def stunted_get():
        raise RuntimeError("Network access not allowed during testing!")

    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: stunted_get())


@pytest.fixture
def scrapper_api() -> TequilaAPI:
    scrapper_config: ConfigHandler = ConfigHandler(ConfigRepo)
    return TequilaAPI(scrapper_config)


@pytest.fixture
def load_response_data() -> dict:
    with open(f"{root_dir}/tests/fixtures/flight_fixture.json", "r") as f:
        data: dict = json.loads(f.read())
    return data


@pytest.fixture
def flight_params() -> dict:
    params: dict = {
        "fly_from": "TFS",
        "fly_to": "KTW",
        "date_from": "25/01/2023",
        "date_to": "30/01/2023",
        "adults": 1,
        "curr": "PLN",
    }
    return params


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):  # noqa
    docker_path: str = os.path.join(
        settings.ROOT_PATH, "tests", "docker-compose-test.yml"
    )
    return docker_path


@pytest.fixture(scope="session")
def test_db_credentials():
    """Returns test database credentials"""
    test_credentials: dict = {
        "NAME": TEST_DB_NAME,
        "USER": TEST_DB_USER,
        "PASSWORD": TEST_DB_PASSWORD,
    }

    return test_credentials


@pytest.fixture(scope="session")
def db_connection(
    docker_services: "Services", docker_ip: str, test_db_credentials: dict
) -> dict:
    """
    :param test_db_credentials:
    :param docker_services: required -> pytest-docker plugin fixture
    :param docker_ip: required -> pytest-docker plugin fixture

    :return dict: db credentials
    """
    user: str = env_values.get("POSTGRES_TEST_USER")
    password: str = env_values.get("POSTGRES_TEST_PASSWORD")
    db_name: str = env_values.get("POSTGRES_TEST_DB_NAME")

    if not user or not db_name or not password:
        raise TestDBWrongCredentialsError()

    port: int = docker_services.port_for("test_db", 5432) or 5450
    credentials: dict = {
        "host": docker_ip,
        "port": port,
        "user": user,
        "password": password,
        "database": db_name,
    }

    # url = f"https://{docker_ip}:{port}"
    # docker_services.wait_until_responsive(
    #     timeout=30.0, pause=0.1, check=lambda: is_responsive(url)
    # )
    return credentials


@pytest.fixture(autouse=True)
def _mock_db_connection(mocker: "MockerFixture", db_connection: dict) -> bool:
    """
    This will alter application database connection settings, once and for all the tests
    in unit tests module.
    :param mocker: pytest-mock plugin fixture
    :param db_connection: connection class
    :return: True upon successful monkey-patching
    """
    mocker.patch("settings.get_db_credentials", db_connection)
    config = settings.DB_CONFIG
    config["connections"]["default"]["credentials"] = db_connection
    mocker.patch("utils.utils.get_db_connections", return_value=config)
    return True


@pytest.fixture
def flight_out_model() -> FlightOut:
    with open(f"{root_dir}/tests/fixtures/flight_out.json", "r") as f:
        data: dict = json.loads(f.read())

    data["response"] = json.dumps(data)
    data.pop("created_at")
    data.pop("updated_at")

    return FlightOut(**data)


@pytest.fixture(autouse=True)
def disable_file_handler(mocker):
    # Replace the FileHandler with a NullHandler that does not write to a file
    mocker.patch.object(logging, "FileHandler", logging.NullHandler)
