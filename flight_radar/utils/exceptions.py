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


class TestDBWrongCredentialsError(CustomBaseException):
    default_message = "Credentials for test DB are wrong. " \
                      "Please be sure that you have valid variables in .env file in root directory"

