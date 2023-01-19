import logging
import os
from typing import List, Dict, Tuple, Type
from urllib import parse as urllib_parse

import sqlalchemy
from databases import Database
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    func,
    Date,
    JSON,
    Float,
    TIMESTAMP,
    DateTime,
)

from settings import get_module_logger, DATABASES
from models.entities import FlightsModel

logger: logging.Logger = get_module_logger("db_config")


class ConfigureTable:
    """Default Table configurator"""

    def __init__(self):
        self.column_type_mapping: Dict = {
            "String": String,
            "Integer": Integer,
            "Date": Date,
            "json": JSON,
            "Float": Float,
        }

    @staticmethod
    def validate_string_field(params_) -> String:
        """Validate if params have max_length arg. If yes, set length to String object"""
        field_type: String = String(params_.get("max_length", 12))
        return field_type

    def __validate_params(self, field_: str) -> Tuple[String | Integer, Dict]:
        """Configuring fields from django-model convention. Fields are configured like:
        date_field = models.DateField(auto_add=True, now=True)
        char_field = models.CharField(max_length=12)
        """
        column_type_: Integer | String | Type[
            TIMESTAMP
        ] | DateTime = self.column_type_mapping.get(
            getattr(getattr(FlightsModel, field_), "type")
        )
        params_: dict = getattr(FlightsModel, field_).__dict__

        if getattr(getattr(FlightsModel, field_), "type") == "String":
            column_type_ = self.validate_string_field(params_)
        if getattr(getattr(FlightsModel, field_), "type") == "Date":
            column_type_ = DateTime(timezone=True)
            if field_ == "created_at":
                ...
                # column_type_ = TIMESTAMP
            if field_ == "updated_at":
                # column_type_ = TIMESTAMP
                params_["onupdate"] = func.current_timestamp()

        if params_.get("type"):
            params_.pop("type")
        if params_.get("max_length"):
            params_.pop("max_length")
        if params_.get("date"):
            params_.pop("date")
        if params_.get("auto_add"):
            params_["server_default"] = func.now()
        if params_.get("auto_add") in (False, True):
            params_.pop("auto_add")

        return column_type_, params_

    def create_table(self) -> Table:
        """Create Table object with specified columns"""
        _metadata = sqlalchemy.MetaData()
        _flights_fields = [
            field
            for field, _ in FlightsModel.__dict__.items()
            if not callable(getattr(FlightsModel, field)) and not field.startswith("__")
        ]

        columns: List[Column] = [
            sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True)
        ]

        for field in _flights_fields:
            column_type: String | Integer
            params: Dict
            column_type, params = self.__validate_params(field)

            columns.append(Column(field, column_type, **params))

        return Table(FlightsModel.__name__.lower(), _metadata, *columns)


class DbInstance:
    """Create DB instance"""

    @staticmethod
    def create_db_instance() -> Database:
        """Returns DB instance"""
        database_dict: dict = DATABASES.get("default")
        db_credentials: str = (
            f"{database_dict.get('USER')}:{database_dict.get('PASSWORD')}"
        )
        db_server_config: str = f"{database_dict.get('HOST')}:{database_dict.get('PORT')}/{database_dict.get('NAME')}"
        ssl_mode: str = urllib_parse.quote_plus(
            str(os.environ.get("ssl_mode", "prefer"))
        )
        database_url: str = f"postgresql://{db_credentials}@{db_server_config}?sslmode={ssl_mode}"  # noqa
        return Database(database_url)


flight_table_schema: Table = ConfigureTable().create_table()
database: Database = DbInstance().create_db_instance()

# engine = sqlalchemy.create_engine(DATABASE_URL, pool_size=3, max_overflow=0)
# engine = create_engine(DATABASE_URL, convert_unicode=True)
# metadata.create_all(engine)


async def db_start() -> None:
    """DB initiator"""
    await database.connect()


async def db_close() -> None:
    """Close DB"""
    await database.disconnect()
