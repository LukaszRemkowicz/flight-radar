import json
import logging
from typing import Optional, List

from databases import Database
from databases.backends.postgres import Record
from sqlalchemy import Table, text, and_
from sqlalchemy.sql import Select, Insert

from errors import InstanceIsNotValid, NoKwargsGiven
from models.entities import FlightsModel, ModelTypes
from models.pydantic_validators import FlightOut, FlightOutList
from settings import DATABASES, get_module_logger
from utils.db_config import database, flight_table_schema

logger: logging.Logger = get_module_logger("db_repo")


class DbRepo:
    """Base DB responsible for returning database instance"""

    db_name: str = DATABASES.get("default").get("NAME")
    table: Optional[Table] = None
    model: ModelTypes = None

    def __init__(self) -> None:
        self.db: Optional[Database] = None

    async def get_database(self) -> Database:
        """Get configured Database"""
        assert self.db_name is not None, f"Please set database. {self.db_name}"
        self.db: Database = database

        return self.db


class BaseRepo(DbRepo):
    async def create(self, data: FlightOut) -> None:
        """Create table row with given parameters"""
        qry: Insert = self.table.insert().values(**data.dict(exclude_none=True))
        db: Database = await self.get_database()
        result: int = await db.execute(qry)
        logger.info(f"New object with id {result} added to DB")

    async def filter(self, **kwargs):
        """Filter DB by given params.
        __in operator:
             - If there is need to find something in list, use it as described: filter(pk__in=[1,2]).
             - Values should be placed in list.
             - Raises InstanceIsNotValid if value is not a list instance
        """

        if not kwargs:
            raise NoKwargsGiven

        db: Database = await self.get_database()
        new_qry: list = []

        for key, value in kwargs.items():
            if "__in" in key:
                if not isinstance(value, List):
                    raise InstanceIsNotValid
                new_qry.extend(
                    [
                        flight_table_schema.c[str(key).replace("__in", "")].in_(value)
                        for key, value in kwargs.items()
                        if "__in" in key
                    ]
                )
            else:
                new_qry.extend(
                    [
                        text(f"{flight_table_schema.c[key]} = '{value}'")
                        for key, value in kwargs.items()
                        if "__in" not in key
                    ]
                )

        qry: Select = self.table.select().where(and_(*new_qry))

        # Filtering by kwargs:
        # qry3 = self.table.select().filter_by(id=1, price=243)

        result: List[Record] = await db.fetch_all(qry)

        if not result:
            return None
        return result


class FlightRepo(BaseRepo):
    table: Table = flight_table_schema
    model: ModelTypes = FlightsModel

    async def filter(self, **kwargs) -> Optional[FlightOutList]:
        """Change DB response for pydantic model"""
        result: List[Record] = await super().filter(**kwargs)
        if not result:
            return None
        new_result: list = []
        for element in result:
            new_element: dict = dict(element)
            new_element["response"] = json.dumps(element["response"])
            new_result.append(new_element)
        FlightOutList(flights=new_result)

        return FlightOutList(flights=new_result)
