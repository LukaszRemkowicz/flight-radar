import logging

import typer

from logger import get_module_logger
from models.schemas import FlightSchema
from models.types import CityTypes
from repos.adapters import TequilaSessionAdapter, TenacityAdapter
from repos.db_repo import FlightRepo, RequestModelRepo
from repos.scrapper import TequilaAPI
from settings import settings
from use_cases.base_use_case import BaseUseCase
from utils.decorators import be_async
from utils.utils import DBConnectionHandler

logger: logging.Logger = get_module_logger("cli")
app = typer.Typer()
tequila_session_adapter = TequilaSessionAdapter()
tenacity: TenacityAdapter = TenacityAdapter()


@app.command()
@be_async
async def get_flights(
    date_from: str = typer.Option(..., "-df", help="Date from. Format: dd-mm-YYYY"),
    date_to: str = typer.Option("", "-dt", help="Date to. Format: dd-mm-YYYY"),
    max_stopovers: int = typer.Option(0, "-s", help="Max stopovers"),
    nights_in_dst_from: int = typer.Option(
        7, "-nif", help="Nights in destination from"
    ),
    nights_in_dst_to: int = typer.Option(10, "-nit", help="Nights in destination to"),
    fly_from: CityTypes = typer.Option("TFS", "-ff", help="Fly from"),
    fly_to: CityTypes = typer.Option("KTW", "-ft", help="Fly to"),
) -> None:
    input_data = FlightSchema(
        date_from=date_from,
        date_to=date_to,
        fly_from=fly_from,
        fly_to=fly_to,
        max_stopovers=max_stopovers,
        nights_in_dst_from=nights_in_dst_from,
        nights_in_dst_to=nights_in_dst_to,
    )

    scrapper_repo = TequilaAPI(
        # retry_policy=tenacity,
        session_adapter=tequila_session_adapter
    )
    await tequila_session_adapter.initialize_session()

    async with DBConnectionHandler():
        flight_use_case: BaseUseCase = BaseUseCase(
            flight_request_repo=RequestModelRepo,
            db_repo=FlightRepo,
            scrapper_repo=scrapper_repo,
        )
        await flight_use_case.get_flights(input_data)

    logger.info("Command get_tfs_data finished with success")


@app.command()
@be_async
async def test():
    """Typer works only if more than one command is defined"""
    scrapper_repo = TequilaAPI(
        # retry_policy=tenacity,
        session_adapter=tequila_session_adapter
    )

    await tequila_session_adapter.initialize_session()
    async with DBConnectionHandler():
        flight_use_case: BaseUseCase = BaseUseCase(
            flight_request_repo=RequestModelRepo,
            db_repo=FlightRepo,
            scrapper_repo=scrapper_repo,
        )
        return await flight_use_case.get_flights({})


if __name__ == "__main__":
    app()
