from datetime import datetime
from typing import Optional, Dict, List

from pydantic import BaseModel, Json


class FlightsBase(BaseModel):
    distance: float
    bags_price: dict
    availability: dict
    airlines: List[str] | dict
    route: List["Dict"]

    booking_token: str
    deep_link: str
    local_arrival: str
    local_departure: str

    price: float


class FlightOut(FlightsBase):
    flight_to_code: str
    flight_from_code: str
    country_to_code: str
    country_from_code: str
    city_from: str
    city_to: str
    bag_limit: dict
    price_conversion: dict
    response: Json
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class FlightOutList(BaseModel):
    flights: List[FlightOut]


class FlightsIn(FlightsBase):
    flyTo: str
    flyFrom: str
    countryTo: dict
    countryFrom: dict
    cityFrom: str
    cityTo: str
    baglimit: dict  # noqa
    conversion: dict


class FlightsListIn(BaseModel):
    flights: List[FlightsIn]
