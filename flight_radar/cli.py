import asyncio
import logging
from asyncio import AbstractEventLoop

import typer

import repos.scrapper as scrapper_repo
import settings as settings
from repos.db_repo import FlightRepo
from use_cases.base_use_case import BaseUseCase
from utils.helpers import DbHandler

logger: logging.Logger = settings.get_module_logger("cli")
app = typer.Typer()


@app.command()
def get_tfs_data(
    date_from: str = typer.Option(..., "-df", help="Date from. Format: dd/mm/YYYY"),
    date_to: str = typer.Option(..., "-dt", help="Date to. Format: dd/mm/YYYY"),
) -> None:
    async def main() -> None:
        async with DbHandler():

            flight_use_case: BaseUseCase = BaseUseCase(
                repo_db=FlightRepo,
                repo_scrapper=scrapper_repo.TequilaAPI,
            )
            await flight_use_case.get_tenerife_flights(
                date_from=date_from, date_to=date_to
            )

        logger.info("Command get_tfs_data finished with success")

    loop: AbstractEventLoop = asyncio.get_event_loop()
    loop.run_until_complete(main())


@app.command()
def test():
    print("working fine")


if __name__ == "__main__":
    app()
