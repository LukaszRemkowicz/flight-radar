from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, field_validator, field_serializer

from models.types import CityTypes


class FlightSchema(BaseModel):
    date_from: str
    date_to: str
    max_stopovers: int
    nights_in_dst_from: int
    nights_in_dst_to: int
    fly_from: CityTypes
    fly_to: CityTypes
    adults: int = 1
    return_from: Optional[date] = None
    return_to: Optional[date] = None
    flight_type: str = "round"
    curr: str = "PLN"
    adult_hand_bag: int = 1
    adult_hold_bag: int = 1

    @field_validator("date_from", "date_to", mode="before")
    @classmethod
    def must_be_valid_date_format(cls, value: str) -> str:
        try:
            datetime.strptime(value, "%d/%m/%Y")
            return value
        except ValueError:
            raise ValueError("Date is in wrong format. Expected: dd/mm/YYYY")
