import json
from typing import List

import pytest
from asyncpg import Record
from databases import Database
from sqlalchemy import Table

from models.pydantic_validators import FlightOut
from repos.db_repo import DbRepo, BaseRepo
from utils.db_config import db_start, db_close


@pytest.mark.asyncio
async def test_db_repo(test_db_credentials) -> None:
    """Test if DB repo is returning database instance. Check if there is connection with db"""

    db_repo: DbRepo() = DbRepo()
    await db_start()
    db_instance = await db_repo.get_database()
    assert db_instance.is_connected
    assert isinstance(db_instance, Database)

    assert test_db_credentials.get('NAME') in db_instance.url.components.path

    await db_close()

    assert not db_instance.is_connected


@pytest.mark.asyncio
async def test_base_repo() -> None:
    """ Test if BaseDB repo is instance of DBRepo """
    db_repo: BaseRepo = BaseRepo()

    assert isinstance(db_repo, BaseRepo)
    assert isinstance(db_repo, DbRepo)


@pytest.mark.asyncio
async def test_creating_document(flight_out_model: FlightOut, table: Table) -> None:
    """ Test if create method work fine """

    await db_start()

    db_repo: BaseRepo = BaseRepo()
    db_instance = await db_repo.get_database()
    db_repo.table = table

    await db_repo.create(flight_out_model)

    qry = table.select()
    result: List[Record] = await db_instance.fetch_all(qry)
    await db_close()

    assert len(result) == 1
    assert result[0].flight_to_code == flight_out_model.flight_to_code
    assert json.loads(result[0].price_conversion) == flight_out_model.price_conversion
