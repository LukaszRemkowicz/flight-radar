from typing import Optional

from databases import Database
from sqlalchemy import Table, text, and_
from sqlalchemy.sql import Select

from models.entities import FlightsModel
from models.pydantic_validators import FlightPydantic
from settings import DATABASES
from utils.db_config import database, flight_table_schema


class DbRepo:
    db_name = DATABASES.get("default").get("NAME")
    table: Optional[Table] = None
    model = None

    def __init__(self):
        self.db: Optional[Database] = None

    async def get_database(self) -> Database:
        assert self.db_name is not None, f"Please set database. {self.db_name=}"
        self.db = database

        return self.db


class BaseRepo(DbRepo):
    async def create(self, data: FlightPydantic) -> None:
        qry = self.table.insert().values(**data.dict(exclude_none=True))
        db = await self.get_database()
        await db.execute(qry)

    async def filter(self, **kwargs):
        db: Database = await self.get_database()
        new_qry = []
        if kwargs:
            for key, value in kwargs.items():
                if "__in" in key and isinstance(value, list):
                    new_qry.extend(
                        [
                            flight_table_schema.c[str(key).replace("__in", "")].in_(
                                value
                            )
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

        result = await db.fetch_all(qry)
        if not result:
            return None
        return result


class FlightRepo(BaseRepo):
    table = flight_table_schema
    model = FlightsModel
