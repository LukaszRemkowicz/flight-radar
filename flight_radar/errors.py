class CustomBaseException(Exception):
    default_message: str = ""

    def __init__(self):
        super().__init__(self.default_message)


class InstanceIsNotValid(CustomBaseException):
    default_message = "Instance is not valid. Should be List instead"


class NoKwargsGiven(CustomBaseException):
    default_message = "There is now kwargs given. Database cant be searched"


class NoFlightWithGivenParams(CustomBaseException):
    default_message = "There is no flights with given params"
