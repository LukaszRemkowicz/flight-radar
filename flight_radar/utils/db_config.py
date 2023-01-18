import logging
import os
from typing import List, Dict, Tuple, Type
from urllib import parse as urllib_parse

import sqlalchemy
from databases import Database
from sqlalchemy import Table, Column, Integer, String, func, Date, JSON, Float, TIMESTAMP, DateTime

from settings import get_module_logger, DATABASES
from models.entities import FlightsModel


def validate_string_field(params_) -> String:
    field_type: String = String(params_.get("max_length", 12))
    return field_type


def validate_params(field_: str) -> Tuple[String | Integer, Dict]:
    column_type_: Integer | String | Type[TIMESTAMP] | DateTime = column_type_mapping.get(
        getattr(getattr(FlightsModel, field_), "type")
    )
    params_: dict = getattr(FlightsModel, field_).__dict__

    if getattr(getattr(FlightsModel, field_), "type") == "String":
        column_type_ = validate_string_field(params_)
    if getattr(getattr(FlightsModel, field_), "type") == "Date":
        column_type_ = DateTime(timezone=True)
        if field_ == 'created_at':
            ...
            # column_type_ = TIMESTAMP
        if field_ == 'updated_at':
            # column_type_ = TIMESTAMP
            params['onupdate'] = func.current_timestamp()

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


logger: logging.Logger = get_module_logger("db_config")
database: dict = DATABASES.get("default")

db_credentials: str = f"{database.get('USER')}:{database.get('PASSWORD')}"
db_server_config: str = (
    f"{database.get('HOST')}:{database.get('PORT')}/{database.get('NAME')}"
)

ssl_mode: str = urllib_parse.quote_plus(str(os.environ.get("ssl_mode", "prefer")))
DATABASE_URL: str = f"postgresql://{db_credentials}@{db_server_config}?sslmode={ssl_mode}"  # type: ignore

database: Database = Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()
column_type_mapping: Dict = {"String": String, "Integer": Integer, "Date": Date, 'json': JSON, 'Float': Float}


flights_fields = [
    field
    for field, _ in FlightsModel.__dict__.items()
    if not callable(getattr(FlightsModel, field)) and not field.startswith("__")
]

columns: List[Column] = [sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True)]

for field in flights_fields:
    column_type: String | Integer
    params: Dict
    column_type, params = validate_params(field)

    columns.append(Column(field, column_type, **params))

flight_table_schema: Table = Table(FlightsModel.__name__.lower(), metadata, *columns)

engine = sqlalchemy.create_engine(DATABASE_URL, pool_size=3, max_overflow=0)
# engine = create_engine(DATABASE_URL, convert_unicode=True)
metadata.create_all(engine)


async def db_start():
    await database.connect()


async def db_close():
    await database.disconnect()
