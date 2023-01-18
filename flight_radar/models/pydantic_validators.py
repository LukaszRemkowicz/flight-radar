from datetime import datetime
from typing import Optional, Dict, List

from pydantic import BaseModel, Json


class FlightPydantic(BaseModel):
    flight_to_code: str
    flight_from_code: str

    country_to_code: str
    country_from_code: str

    city_from: str
    city_to: str

    distance: float

    bags_price: dict
    bag_limit: dict

    availability: dict
    airlines: dict
    route: List['Dict']

    booking_token: str
    deep_link: str
    local_arrival: str
    local_departure: str

    price: float
    price_conversion: dict

    response: Json
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
