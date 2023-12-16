import json
import logging
from typing import Type

from logger import get_module_logger
from models.entities import (
    TequilaFlightList,
    TequilaFlightRoutes,
    TequilaFlightResponse,
    BaseFlightModel,
    RequestSchema,
)
from models.models import Flight
from models.schemas import FlightSchema
from repos import ReposTypes
from repos.adapters import TequilaSessionAdapter, TenacityAdapter
from repos.db_repo import FlightRepo, FlightProtocol
from utils.exceptions import NoFlightWithGivenParams

logger: logging.Logger = get_module_logger("base_use_case")


tequila_session_adapter = TequilaSessionAdapter()


class BaseUseCase:
    def __init__(
        self,
        flight_request_repo: Type[FlightProtocol],
        db_repo: Type[FlightProtocol],
        scrapper_repo,
    ) -> None:
        self.request_repo: FlightProtocol = flight_request_repo()
        self.db_repo: FlightProtocol = db_repo()
        self.scrapper_repo = scrapper_repo

    async def get_flights(self, input_data: FlightSchema) -> None:
        """Get flights from scrapper and save to DB"""

        # aaa = await self.scrapper_repo.get_destination_code("Gdansk")
        # breakpoint()
        # return aaa

        # kwargs_for_search: dict = {
        #     "fly_from": input_data.fly_from,
        #     "fly_to": input_data.fly_to,
        #     "date_from": input_data.date_from.strftime("%d/%m/%Y"),
        #     # "date_to": date_to.strftime("%d/%m/%Y"),
        #     # "return_from": (date_to - timedelta(days=3)).strftime("%d/%m/%Y"),
        #     # "return_to": (date_to + timedelta(days=3)).strftime("%d/%m/%Y"),
        #     "adults": input_data.adults,
        #     "nights_in_dst_from": input_data.nights_in_dst_from,
        #     "nights_in_dst_to": input_data.nights_in_dst_to,
        #     "flight_type": "round",
        #     "curr": "PLN",
        #     "max_stopovers": input_data.max_stopovers,
        #     "adult_hand_bag": 1,
        #     "adult_hold_bag": 1,
        # }
        kwargs_for_search = input_data.model_dump(exclude_none=True)

        # if input_data.date_to:
        #     kwargs_for_search["date_to"] = input_data.date_to.strftime("%d/%m/%Y")

        flight_list: TequilaFlightList = await self.scrapper_repo.get_flight(
            kwargs_for_search
        )

        if not flight_list or not flight_list.flights:
            raise NoFlightWithGivenParams

        request_obj = await self.request_repo.create(
            data=RequestSchema(
                request_id=flight_list.search_id,
                response=flight_list.model_dump(),
                requested_flight_to=input_data.fly_to,
                requested_flight_from=input_data.fly_from,
            )
        )

        for flight in flight_list.flights:
            breakpoint()

            routes: list[TequilaFlightRoutes] = flight.route
            flight.route = list()

            breakpoint()
            aa = await self.db_repo.create(data=flight)

            new_val: FlightOut = FlightOut(**new_flight_data)

            search_params = {
                "flight_from_code": input_data.fly_from,
                "flight_to_code": input_data.fly_to,
                "price": flight.price,
                "local_departure": flight.local_departure,
                "local_arrival": flight.local_arrival,
            }
            # TODO dodac flight to a pozniej flight from z foreignkeyem

            exists = await self.db_repo.filter(**search_params)
            if exists:
                continue
            await self.db_repo.create(new_val)
        # exists = await self.db_repo.filter(id__in=[element for element in range(1000)], price=300)
