import logging
import os
from time import sleep
from typing import List, Dict, Tuple, Type, Optional
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
    DateTime, create_engine,
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
        self.model = FlightsModel
        self.db_name: Optional[str] = None

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
        try:
            column_type_: Integer | String | Type[
                TIMESTAMP
            ] | DateTime = self.column_type_mapping.get(
                getattr(getattr(self.model, field_), "type_class")
            )
        except AttributeError:
            breakpoint()

        params_: dict = getattr(self.model, field_).__dict__

        if getattr(getattr(self.model, field_), "type_class") == "String":
            # if not params_.get('max_length'):
            #     breakpoint()
            column_type_ = self.validate_string_field(params_)

        if getattr(getattr(self.model, field_), "type_class") == "Date":
            column_type_ = DateTime(timezone=True)
            if field_ == "created_at":
                params_["server_default"] = func.now()
                # column_type_ = TIMESTAMP
            if field_ == "updated_at":
                # column_type_ = TIMESTAMP
                params_["onupdate"] = func.current_timestamp()

        if params_.get("type_class"):
            params_.pop("type_class")
        if params_.get("max_length"):
            params_.pop("max_length")
        if params_.get("date"):
            params_.pop("date")
        if params_.get("auto_add"):
            params_["server_default"] = func.now()
        if params_.get("auto_add") in (False, True):
            params_.pop("auto_add")

        return column_type_, params_

    def set_up_db_name(self, name: Optional[str] = None):
        """Returns db name"""
        if not name:
            self.db_name = self.model.__name__.lower()
        else:
            self.db_name = name

    def create_table(self) -> Table:
        """Create Table object with specified columns"""
        _metadata = sqlalchemy.MetaData()
        _flights_fields = [
            field
            for field, _ in self.model.__dict__.items()
            if not callable(getattr(self.model, field)) and not field.startswith("__")
        ]

        columns: List[Column] = [
            sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True)
        ]

        for field in _flights_fields:
            column_type: String | Integer
            params: Dict
            column_type, params = self.__validate_params(field)

            columns.append(Column(field, column_type, **params))
        self.set_up_db_name()

        return Table(self.db_name, _metadata, *columns)


class DbInstance:
    """Create DB instance"""

    def __init__(self, config: Optional[dict] = None):
        self.db_config = config or DATABASES
        self.db_url: Optional[str] = None

    def get_db_url(self):
        database_dict: dict = self.db_config.get("default")
        db_credentials: str = (
            f"{database_dict.get('USER')}:{database_dict.get('PASSWORD')}"
        )
        db_server_config: str = f"{database_dict.get('HOST')}:{database_dict.get('PORT')}/{database_dict.get('NAME')}"
        # ssl_mode: str = urllib_parse.quote_plus(
        #     str(os.environ.get("ssl_mode", "prefer"))
        # )
        database_url: str = f"postgresql+asyncpg://{db_credentials}@{db_server_config}"  # noqa
        return database_url

    def create_db_instance(self) -> Database:
        """Returns DB instance"""
        # database_dict: dict = self.db_config.get("default")
        # db_credentials: str = (
        #     f"{database_dict.get('USER')}:{database_dict.get('PASSWORD')}"
        # )
        # db_server_config: str = f"{database_dict.get('HOST')}:{database_dict.get('PORT')}/{database_dict.get('NAME')}"
        # ssl_mode: str = urllib_parse.quote_plus(
        #     str(os.environ.get("ssl_mode", "prefer"))
        # )
        # database_url: str = f"postgresql://{db_credentials}@{db_server_config}?sslmode={ssl_mode}"  # noqa
        # self.db_url = database_url

        return Database(self.get_db_url())

# db_instance: DbInstance = DbInstance()


if not os.environ.get('TEST'):
    database: Database = DbInstance().create_db_instance()
    flight_table_schema: Table = ConfigureTable().create_table()
    # metadata = MetaData()
    # engine = create_engine(db_instance.get_db_url())
    # metadata.create_all(engine)
    metadata = sqlalchemy.MetaData()
    engine = create_engine(DbInstance().get_db_url())
    metadata.create_all(engine)
else:
    database: None = None
    flight_table_schema: None = None

# engine = sqlalchemy.create_engine(DATABASE_URL, pool_size=3, max_overflow=0)


async def db_start() -> None:
    """DB initiator"""
    sleep(2)
    await database.connect()


async def db_close() -> None:
    """Close DB"""
    sleep(2)
    await database.disconnect()
