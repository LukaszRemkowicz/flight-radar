import json
from datetime import datetime
from typing import Type

from models.config import ConfigRepo
from models.pydantic_validators import FlightPydantic
from repos.db_repo import FlightRepo
from repos.scrapper_config_handler import ConfigHandler
from repos import ReposTypes
from utils.helpers import field_mapper


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
        kwargs = {
            "fly_from": "TFS",
            "fly_to": "KTW",
            "date_from": params.get("date_from"),
            "date_to": params.get("date_to"),
            "adults": params.get("adults", 1),
            "curr": "PLN",
        }

        data = await self.scrapper_repo.get_flight(kwargs)
        if data:
            for flight in data.get('data'):
                flight['response'] = json.dumps(flight)
                new_flight_data: dict = field_mapper(flight)
                new_flight_data['date_from'] = datetime.strptime(params.get("date_from"), '%d/%m/%Y')
                new_flight_data['date_to'] = datetime.strptime(params.get("date_to"), '%d/%m/%Y')
                new_val = FlightPydantic(**new_flight_data)

                search_params = {
                    "flight_from_code": "TFS",
                    "flight_to_code": "KTW",
                    "price": data.get("price"),
                    "local_departure": data.get("local_departure"),
                    "local_arrival": data.get("local_arrival"),
                }

                exists = await self.db_repo.filter(**search_params)
                if exists:
                    breakpoint()

                await self.db_repo.create(new_val)
            # return await self.scrapper_repo.get_flight(kwargs)
        # exists = await self.db_repo.filter(id__in=[element for element in range(1000)], price=300)

