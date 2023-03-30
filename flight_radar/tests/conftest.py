import asyncio
import json
import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import sqlalchemy
from sqlalchemy import Table

import flight_radar.errors as errors

os.environ["TEST"] = "True"

import requests
from databases import Database

import flight_radar.settings as settings
import pytest

if TYPE_CHECKING:
    from pytest_docker.plugin import Services, MockerFixture

root_dir = settings.ROOT_PATH
sys.path.append(root_dir)

from flight_radar.utils.db_config import DbInstance, ConfigureTable
from utils.scrapper_config import ConfigRepo  # noqa
from models.entities import FlightOut
from repos.scrapper import TequilaAPI  # noqa
from repos.scrapper_config_handler import ConfigHandler  # noqa

from dotenv import dotenv_values

env_path: str = os.path.join(str(Path(root_dir).parent), ".env")
env_values = dict(dotenv_values(env_path))

TEST_DB_PASSWORD = env_values.get("POSTGRES_TEST_PASSWORD")
TEST_DB_USER = env_values.get("POSTGRES_TEST_USER")
TEST_DB_NAME = env_values.get("POSTGRES_TEST_DB_NAME")


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
    docker_path: str = os.path.join(str(pytestconfig.rootdir), "docker-compose.yml")
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
) -> Database:
    """
    :param test_db_credentials:
    :param docker_services: required -> pytest-docker plugin fixture
    :param docker_ip: required -> pytest-docker plugin fixture

    :return Daabase: db instance
    """
    # new_config = {
    #     'default': {
    #         'NAME': 'postgres',
    #         'USER': 'postgres',
    #         'HOST': docker_ip,
    #         'PASSWORD': settings.TEST_DB_PASSWORD,
    #         'PORT': docker_services.port_for('test_db', 5430) or 5430,
    #     }
    # }
    if (
        not test_db_credentials.get("USER")
        or not test_db_credentials.get("NAME")
        or not test_db_credentials.get("PASSWORD")
    ):
        raise errors.TestDBWrongCredentialsError()

    new_config = {
        "default": {
            **test_db_credentials,
            "HOST": docker_ip,
            "PORT": docker_services.port_for("test_db", 5430) or 5430,
        }
    }
    db_instance: DbInstance = DbInstance(new_config)
    database: Database = db_instance.create_db_instance()

    async def main():
        from sqlalchemy.dialects import postgresql

        metadata = sqlalchemy.MetaData()
        dialect = postgresql.dialect()

        table_obj: ConfigureTable = ConfigureTable()
        # table_obj.set_up_db_name(TEST_DB_NAME)
        table: Table = table_obj.create_table()
        await asyncio.sleep(2)
        await database.connect()

        schema = sqlalchemy.schema.CreateTable(table, if_not_exists=True)
        query = str(schema.compile(dialect=dialect))
        await database.execute(query=query)
        await database.disconnect()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    #
    # database.execute(CreateTable(table))
    # database.disconnect()
    # engine = create_engine(
    #     db_instance.get_db_url(),
    # )
    #
    # conn = engine.connect()
    #
    # database.execute(CreateTable(table))
    # # metadata = sqlalchemy.MetaData()
    # # engine = create_engine(db_instance.get_db_url())
    # # metadata.create_all(engine)
    #
    # database.disconnect()

    # database = await db_start()
    return database


@pytest.fixture(autouse=True)
def _mock_db_connection(mocker: "MockerFixture", db_connection: Database) -> bool:
    """
    This will alter application database connection settings, once and for all the tests
    in unit tests module.
    :param mocker: pytest-mock plugin fixture
    :param db_connection: connection class
    :return: True upon successful monkey-patching
    """
    mocker.patch("utils.db_config.database", db_connection)
    return True


@pytest.fixture(scope="session")
def table() -> Table:

    table_obj: ConfigureTable = ConfigureTable()
    # table_obj.set_up_db_name(TEST_DB_NAME)
    table: Table = table_obj.create_table()

    return table


@pytest.fixture(autouse=True)
def _mock_table_creation(mocker: "MockerFixture", table):
    """
    This will create database table instance for all the tests.
    :param mocker: pytest-mock plugin fixture
    :param table_creation
    :return: True upon successful monkey-patching
    """

    # mocker.patch('utils.db_config.ConfigureTable.db_name', return_value=TEST_DB_NAME)
    # # mocker.patch.object(ConfigureTable, 'db_name', new_callable=PropertyMock(return_value=TEST_DB_NAME))

    mocker.patch.object(ConfigureTable, "create_table", return_value=table)
    mocker.patch("utils.db_config.flight_table_schema", table)

    return True


@pytest.fixture
def flight_out_model() -> FlightOut:
    with open(f"{root_dir}/tests/fixtures/flight_out.json", "r") as f:
        data: dict = json.loads(f.read())

    data["response"] = json.dumps(data)
    data.pop("created_at")
    data.pop("updated_at")

    return FlightOut(**data)
