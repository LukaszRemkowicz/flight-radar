import logging

import typer

from repos.scrapper import TequilaAPI
import settings as settings
from repos.db_repo import FlightRadarRepo
from use_cases.base_use_case import BaseUseCase
from utils.decorators import be_async
from utils.utils import DBConnectionHandler, DataInputValidation

logger: logging.Logger = settings.get_module_logger("cli")
app = typer.Typer()


@app.command()
@be_async
async def get_tfs_data(
    date_from: str = typer.Option(..., "-df", help="Date from. Format: dd/mm/YYYY"),
    date_to: str = typer.Option(..., "-dt", help="Date to. Format: dd/mm/YYYY"),
) -> None:

    async with DataInputValidation(date_to):
        ...
    async with DataInputValidation(date_from):
        ...

    async with DBConnectionHandler():

        flight_use_case: BaseUseCase = BaseUseCase(
            repo_db=FlightRadarRepo,
            repo_scrapper=TequilaAPI,
        )
        await flight_use_case.get_tenerife_flights(date_from=date_from, date_to=date_to)

    logger.info("Command get_tfs_data finished with success")


@app.command()
def test():
    print("working fine")


if __name__ == "__main__":
    app()
