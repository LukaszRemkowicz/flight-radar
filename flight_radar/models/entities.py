import json
from datetime import date
from typing import List, Optional, Union

from pydantic import BaseModel, Json, Field

from settings import MockedUsers


class TequilaFlightRoutes(BaseModel):
    fly_from_city: str = Field(alias="cityFrom")
    fly_to_city: str = Field(alias="cityTo")
    local_departure: str
    local_arrival: str
    utc_departure: str
    utc_arrival: str
    airline: str
    flight_no: int
    return_: int = Field(alias="return")


class BaseFlightModel(BaseModel):
    search_id: str = Field(alias="id")
    fly_from: str = Field(alias="flyFrom")
    fly_to: str = Field(alias="flyTo")
    city_from: str = Field(alias="cityFrom")
    city_to: str = Field(alias="cityTo")
    nights: int = Field(alias="nightsInDest")
    bags_price: dict
    bag_limit: dict = Field(alias="baglimit")
    availability: dict
    airlines: List[str]
    # route: List[TequilaFlightRoutes]
    booking_token: str
    deep_link: str
    price: float
    price_conversion: dict = Field(alias="conversion")
    local_arrival: str
    local_departure: str


class TequilaFlightResponse(BaseFlightModel):
    """Response from tequila api"""

    # id_: str = Field(alias="id")
    # fly_from: str = Field(alias="flyFrom")
    # fly_to: str = Field(alias="flyTo")
    # city_from: str = Field(alias="cityFrom")
    # city_to: str = Field(alias="cityTo")
    # nights: int = Field(alias="nightsInDest")
    # price: float
    # conversion: dict
    # bags_price: dict
    # bag_limit: dict = Field(alias="baglimit")
    # availability: dict
    # airlines: List[str]
    # booking_token: str
    # deep_link: str
    # utc_departure: str
    # utc_arrival: str
    route: List[TequilaFlightRoutes]

    def dump_to_model(self):
        """
        Dump airlines to json.
        Method used for Postgresql, because it is not possible to store list in DB
        """
        self.airlines = json.dumps(self.airlines)
        return self


class TequilaFlightList(BaseModel):
    search_id: str
    flights: List[TequilaFlightResponse]


class FlightRoutesFromDB(TequilaFlightRoutes):
    id: int
    created_at: date
    updated_at: Optional[date]


class FlightRoutesFromDBList(BaseModel):
    flights: List[FlightRoutesFromDB]


class RequestSchema(BaseModel):
    request_id: str
    response: dict
    requested_flight_to: str
    requested_flight_from: str
    user_id: int = MockedUsers.ANONYMOUS_USER  # right now, user feature is not implemented


SCHEMAS_TYPES = Union[TequilaFlightResponse, TequilaFlightRoutes, RequestSchema]
