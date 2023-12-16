from typing import Union

from tortoise import Model, fields


class RequestModel(Model):
    request_id = fields.CharField(
        max_length=124,
        description="Search ID. Example: a4fd41e0-6f06-8de2-b4bc-b5c0440cca0b",
        unique=True,
    )
    response = fields.JSONField()
    requested_flight_to = fields.CharField(max_length=124)
    requested_flight_from = fields.CharField(max_length=124)
    user_id = fields.IntField()

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    @classmethod
    async def create(cls, **kwargs):
        return await super().create(**kwargs)


class Flight(Model):
    search_id = fields.ForeignKeyField(
        "models.RequestModel",
        related_name="request",
        on_delete=fields.CASCADE,
        null=True,
    )
    fly_from = fields.CharField(
        max_length=12, description="Country to code. Example: PL"
    )
    fly_to = fields.CharField(
        max_length=12, description="Country from code. Example: ES"
    )
    city_from = fields.CharField(
        max_length=124, description="City from. Example: Warsaw"
    )
    city_to = fields.CharField(max_length=124, description="City to. Example: Tenerife")
    nights: int = fields.IntField()

    bags_price = fields.JSONField()
    bag_limit = fields.JSONField()

    availability = fields.JSONField()
    airlines = fields.JSONField()
    # route = fields.JSONField()

    booking_token = fields.CharField(max_length=2048)
    deep_link = fields.CharField(max_length=2048)

    price = fields.FloatField()
    price_conversion = fields.JSONField()

    local_arrival = fields.CharField(
        max_length=1024, description="Local arrival time. Example: 2021-07-10T23:10"
    )
    local_departure = fields.CharField(
        max_length=1024, description="Local departure time. Example: 2021-07-10T23:10"
    )

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "flights"

    @classmethod
    async def create(cls, **kwargs):
        return await super().create(**kwargs)


class FlightRoute(Model):
    """Stores flight route data (there and back)"""

    city_from = fields.CharField(
        max_length=124, description="City from. Example: Warsaw"
    )
    city_to = fields.CharField(max_length=124, description="City to. Example: Tenerife")

    airline = fields.CharField(max_length=100, description="Airline. Example: Ryanair")

    return_ = fields.BooleanField(description="Return flight. Example: True")

    flight_no = fields.CharField(
        max_length=124, description="Flight number. Example: FR 321"
    )
    local_arrival = fields.CharField(
        max_length=1024, description="Local arrival time. Example: 2021-07-10T23:10"
    )
    local_departure = fields.CharField(
        max_length=1024, description="Local departure time. Example: 2021-07-10T23:10"
    )

    flight = fields.ForeignKeyField(
        "models.Flight",
        related_name="flight",
        on_delete=fields.CASCADE,
        null=True,
    )

    class Meta:
        table = "flight_route"


ModelTypes = FlightRoute | Flight | RequestModel
