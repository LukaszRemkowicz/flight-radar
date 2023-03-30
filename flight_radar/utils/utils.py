from typing import Optional

from models.entities import FlightsIn
import logging

from tortoise import Tortoise
from asyncpg import CannotConnectNowError

from utils.exceptions import DBConnectionError, ValidationError
from settings import get_module_logger, DB_CONFIG

logger: logging.Logger = get_module_logger("utils")


def field_mapper(data: FlightsIn) -> dict:
    """Basic field mapper. Function maps API response fields to more pydantic convention"""
    new_data: dict = data.dict()
    if data.flyFrom:
        new_data["flight_from_code"] = data.flyFrom
    if data.flyTo:
        new_data["flight_to_code"] = data.flyTo
    if data.cityFrom:
        new_data["city_from"] = data.cityFrom
    if data.cityTo:
        new_data["city_to"] = data.cityTo
    if data.baglimit:
        new_data["bag_limit"] = data.baglimit
    if data.conversion:
        new_data["price_conversion"] = data.conversion
    if data.countryTo:
        new_data["country_to_code"] = data.countryTo.get("code")
    if data.countryFrom:
        new_data["country_from_code"] = data.countryFrom.get("code")

    return new_data


class DBConnectionHandler:
    """Handler responsible for connection and disconnection to database"""

    async def __aenter__(self) -> None:
        """Open database connection"""
        await Tortoise.init(config=DB_CONFIG)
        while True:
            retry: int = 0
            try:
                if retry >= 5:
                    raise DBConnectionError()
                await Tortoise.generate_schemas()
                break
            except (ConnectionError, CannotConnectNowError):
                retry += 1
                pass

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Close database connection"""
        await Tortoise.close_connections()


class DataInputValidation:

    def __init__(self, date: Optional[str]):
        self.date = date
        self.date_error_msg: str = 'Date is in wrong format'

    def validate_date(self):
        if self.date:
            date_len: list = self.date.split('/')
            if len(date_len) != 3:
                raise ValidationError(f'{self.date_error_msg}: Expected format: dd/mm/YYYY')
            elif len(date_len) == 3:
                if not date_len[0].isdigit() or len(date_len[0]) > 2:
                    raise ValidationError(f'Day is in wrong format.')
                if int(date_len[0]) >= 32:
                    raise ValidationError(f"Day is in wrong format: Can't be higher than 31")
                if not date_len[1].isdigit() or len(date_len[0]) > 2:
                    raise ValidationError(f'Month is in wrong format.')
                if int(date_len[1]) >= 12:
                    raise ValidationError(f"Month is in wrong format: Can't be higher than 12")
                if not date_len[2].isdigit() or len(date_len[0]) > 4:
                    raise ValidationError(f'Year is in wrong format.')

    async def __aenter__(self) -> None:
        self.validate_date()

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        ...
