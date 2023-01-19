import json
import logging
from typing import Type

from errors import NoFlightWithGivenParams
from models.config import ConfigRepo
from models.pydantic_validators import FlightOut, FlightsListIn
from repos.db_repo import FlightRepo
from repos.scrapper_config_handler import ConfigHandler
from repos import ReposTypes
from settings import get_module_logger
from utils.helpers import field_mapper

logger: logging.Logger = get_module_logger("base_use_case")


class BaseUseCase:
    def __init__(
        self,
        repo_db: Type[FlightRepo],
        repo_scrapper: Type[ReposTypes],
    ) -> None:
        self.db_repo = repo_db()
        self.__scrapper_config: ConfigHandler = ConfigHandler(ConfigRepo)
        self.scrapper_repo = repo_scrapper(self.__scrapper_config)

    async def get_tenerife_flights(self, **params):
        """Main Tenerife Flights method"""

        kwargs: dict = {
            "fly_from": "TFS",
            "fly_to": "KTW",
            "date_from": params.get("date_from"),
            "date_to": params.get("date_to"),
            "adults": params.get("adults", 1),
            "curr": "PLN",
        }

        flight_list: FlightsListIn = await self.scrapper_repo.get_flight(kwargs)
        if not flight_list or not flight_list.flights:
            raise NoFlightWithGivenParams

        for flight in flight_list.flights:

            new_flight_data: dict = field_mapper(flight)
            new_flight_data["response"] = json.dumps(flight.dict())
            new_val: FlightOut = FlightOut(**new_flight_data)

            search_params = {
                "flight_from_code": "TFS",
                "flight_to_code": "KTW",
                "price": flight.price,
                "local_departure": flight.local_departure,
                "local_arrival": flight.local_arrival,
            }

            exists = await self.db_repo.filter(**search_params)
            if exists:
                continue

            await self.db_repo.create(new_val)
        # exists = await self.db_repo.filter(id__in=[element for element in range(1000)], price=300)
