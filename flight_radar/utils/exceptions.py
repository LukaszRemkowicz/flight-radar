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
    default_message = (
        "Credentials for test DB are wrong. "
        "Please be sure that you have valid variables in .env file in root directory"
    )


class InstanceIsNotValid(CustomBaseException):
    default_message = "Instance is not valid. Should be List instead"


class NoKwargsGiven(CustomBaseException):
    default_message = "There is now kwargs given. Database cant be searched"


class NoFlightWithGivenParams(CustomBaseException):
    default_message = "There is no flights with given params"
