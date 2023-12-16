import json
import logging
from typing import List, Optional, Protocol

from logger import get_module_logger
from models.entities import (
    FlightRoutesFromDBList,
    SCHEMAS_TYPES, BaseFlightModel,
)

from models.models import Flight, RequestModel

logger: logging.Logger = get_module_logger("db_repo")


class FlightProtocol(Protocol):
    async def create(self, data: SCHEMAS_TYPES) -> BaseFlightModel:
        ...

    async def filter(self, **kwargs) -> BaseFlightModel | None:
        ...


class RequestModelRepo:
    model = RequestModel

    async def create(self, data: SCHEMAS_TYPES) -> BaseFlightModel:
        """Save flight to DB"""

        flight_data = data.model_dump()
        res: RequestModel = await self.model.create(**flight_data)
        return res

    async def filter(self, **kwargs) -> SCHEMAS_TYPES | None:
        ...

class FlightRepo:
    model = Flight

    async def create(self, data: SCHEMAS_TYPES) -> BaseFlightModel:
        """Save flight to DB"""

        flight_data = data.model_dump(exclude={"route"})
        breakpoint()
        res: Flight = await self.model.create(**flight_data)  # noqa
        logger.info(f"New object with id {res.pk} added to DB")

        return BaseFlightModel(**res.__dict__)

    async def filter(self, **kwargs) -> SCHEMAS_TYPES | None:
        """Filter by given params."""

        res: List[Flight] = await self.model.filter(**kwargs)
        if not res:
            return None
        new_result: list = []
        for element in res:
            new_element: dict = dict(element)
            new_element["response"] = json.dumps(element.response)
            new_result.append(new_element)
        FlightRoutesFromDBList(flights=new_result)

        return FlightRoutesFromDBList(flights=new_result)
