import asyncio
import logging

import typer

import repos.scrapper as scrapper_repo
import settings as settings
from repos.db_repo import FlightRepo
from use_cases.base_use_case import BaseUseCase
from utils.db_config import db_start, db_close

logger: logging.Logger = settings.get_module_logger("cli")
app = typer.Typer()


@app.command()
def get_tfs_data():
    async def main() -> None:
        await db_start()

        flight_use_case = BaseUseCase(
            repo_db=FlightRepo,
            repo_scrapper=scrapper_repo.TequilaAPI,
        )
        kwargs = {
            "date_from": '20/01/2023',
            "date_to": '30/01/2023',
        }
        data = await flight_use_case.get_tenerife_flights(**kwargs)
        await db_close()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


@app.command()
def test():
    print("working fine")


if __name__ == "__main__":
    app()
