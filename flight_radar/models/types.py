from datetime import datetime
from random import choice
from typing import Dict, Optional, Type

from pydantic import BaseModel


class UrlConfigs:
    TEQUILA_URL = "https://api.tequila.kiwi.com/v2/search?"


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
    min_wait_between: int
    max_wait_between: int
    min_wait_before: int
    max_wait_before: int
    max_attempts: int


class RequestHeaders(BaseModel):
    """Headers params"""

    user_agent: str = None
    origin: str = ORIGIN
    accept: str = "application/json, text/plain, */*"
    accept_encoding: str = "gzip, deflate, br"
    accept_language: str = "en-US,en;q=0.9,pl;q=0.8"
    method: str = "GET"

    def __call__(self) -> Dict:
        """set different user agent on every object call"""
        self.set_user_agent()
        return self.dict()

    def set_user_agent(self) -> None:
        """shuffle user agent"""
        self.user_agent = choice(USER_AGENTS)

    def dict(self, **kwargs):
        """
        properly serialized headers
        """
        serialized = super().dict()
        serialized["User-agent"] = serialized.pop("user_agent")
        return serialized


class CharFieldModel:
    type_class = "String"

    def __init__(
        self,
        max_length: int = 0,
        primary_key: bool = False,
        default: Optional[str] = None,
    ):
        self.max_length = max_length
        self.primary_key = primary_key
        self.default = default


class IntegerFieldModel:
    type_class = "Integer"

    def __init__(self, primary_key: bool = False):
        self.primary_key = primary_key


class FloatFieldModel:
    type_class = "Float"


class DateFieldModel:
    type_class = "Date"

    def __init__(
        self,
        date: Optional[str] = None,
        auto_add: bool = False,
        now: bool = False,
    ):
        if now:
            self.date = datetime.now()
        elif date:
            self.validate_date()
            self.date = date
        self.auto_add = auto_add

    def validate_date(self):
        try:
            datetime.strptime("%d/%m/%Y", self.date)
        except ValueError:
            breakpoint()
            raise ValueError


class JsonFieldModel:
    type_class = "json"


class Models:
    def __init__(
        self,
        char_field: Type[CharFieldModel],
        integer_field: Type[IntegerFieldModel],
        date_field: Type[DateFieldModel],
        float_field: Type[FloatFieldModel],
        json_field: Type[JsonFieldModel],
    ):
        self.CharField = char_field
        self.IntegerField = integer_field
        self.DateField = date_field
        self.FloatField = float_field
        self.JsonField = json_field


models = Models(
    CharFieldModel, IntegerFieldModel, DateFieldModel, FloatFieldModel, JsonFieldModel
)
