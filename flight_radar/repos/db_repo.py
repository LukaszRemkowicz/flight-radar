import json
import logging
from typing import Optional, List

from models.models import FlightsModel
from models.entities import FlightOut, FlightOutList
from settings import get_module_logger

logger: logging.Logger = get_module_logger("db_repo")


class FlightRadarRepo:

    model = FlightsModel

    async def create(self, data: FlightOut) -> FlightsModel:
        """Save flight to DB"""
        res: FlightsModel = await self.model.create(**data.dict())  # noqa
        logger.info(f"New object with id {res.pk} added to DB")
        return res

    async def filter(self, **kwargs) -> Optional[FlightOutList]:
        """Filter by given params."""

        res: List[FlightsModel] = await self.model.filter(**kwargs)
        if not res:
            return None
        new_result: list = []
        for element in res:
            new_element: dict = dict(element)
            new_element["response"] = json.dumps(element.response)
            new_result.append(new_element)
        FlightOutList(flights=new_result)

        return FlightOutList(flights=new_result)
