from enum import StrEnum
from random import choice
from typing import Dict, Optional

from pydantic import BaseModel


class TequilaUrls:
    BASE_URL = "https://api.tequila.kiwi.com/"
    FLIGHT_SEARCH = BASE_URL + "v2/search?"
    FIND_LOCATION = BASE_URL + "locations/query?"


ORIGIN: str = ""

USER_AGENTS: list = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 "
    "Safari/537.36 Edge/14.14393",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 "
    "Mobile/14E304 Safari/602.1",
]


class Config(BaseModel):
    MIN_WAIT_BETWEEN: int
    MAX_WAIT_BETWEEN: int
    MIN_WAIT_BEFORE: int
    MAX_WAIT_BEFORE: int
    MAX_ATTEMPTS: int


class RequestHeaders(BaseModel):
    """Headers params"""

    user_agent: Optional[str] = None
    origin: str = ORIGIN
    accept: str = "application/json, text/plain, */*"
    accept_encoding: str = "gzip, deflate, br"
    accept_language: str = "en-US,en;q=0.9,pl;q=0.8"
    method: str = "GET"

    def __call__(self) -> Dict:
        """call different user agent on every object call"""
        self.set_user_agent()
        return self.dict()

    def set_user_agent(self) -> None:
        """shuffle user agent"""
        self.user_agent = choice(USER_AGENTS)

    def dict(self, **kwargs):
        """serialize headers"""
        serialized = super().model_dump()
        serialized["User-agent"] = serialized.pop("user_agent")
        return serialized


class CityTypes(StrEnum):
    """City types"""

    WARSZAWA_MODLIN = "WMI"
    TENERIFE = "TFS"
    KATOVICE = "KTW"
