from typing import Optional

import pytest
from models.entities import FlightOut, FlightOutList
from repos.db_repo import FlightRepo
from utils.utils import DBConnectionHandler


@pytest.mark.asyncio
async def test_creating_document(flight_out_model: FlightOut) -> None:
    """Test create and filter methods for DB repo"""

    async with DBConnectionHandler():
        db_repo: FlightRepo = FlightRepo()
        res_obj = await db_repo.create(flight_out_model)

        result: Optional[FlightOutList] = await db_repo.filter(pk=res_obj.pk)

        assert isinstance(result, FlightOutList)
        assert isinstance((obj := result.flights[0]), FlightOut)
        assert obj.flight_to_code == flight_out_model.flight_to_code
        assert obj.price == flight_out_model.price
