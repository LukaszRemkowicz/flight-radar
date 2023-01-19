from models.pydantic_validators import FlightsIn
from utils.db_config import db_close, db_start


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


class DbHandler:
    """Handler responsible for connection and disconnection to database"""

    async def __aenter__(self) -> None:
        """Open database connection"""
        return await db_start()

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Close database connection"""
        await db_close()
