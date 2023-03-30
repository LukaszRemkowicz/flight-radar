from asyncpg import CannotConnectNowError


class CustomBaseException(Exception):
    default_message: str = ""

    def __init__(self):
        super().__init__(self.default_message)


class DBConnectionError(ConnectionError, CannotConnectNowError):
    default_message = str(CannotConnectNowError)


class BadRequestException(Exception):
    ...


class ValidationError(Exception):
    ...
