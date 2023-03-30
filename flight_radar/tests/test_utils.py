import pytest
from tortoise import Tortoise, connections

from tests.conftest import env_values
from utils.utils import DBConnectionHandler


@pytest.mark.asyncio
async def test_db_handler():
    """Test if handler is handling connection to DB"""

    assert not Tortoise.is_connected  # noqa

    async with DBConnectionHandler():
        assert Tortoise.is_connected  # noqa
        assert Tortoise.get_connection("default").database == env_values.get(  # noqa
            "POSTGRES_TEST_DB_NAME"
        )
