from typing import Union

from tortoise import fields, Model


class FlightsModel(Model):
    flight_to_code = fields.CharField(max_length=12)
    flight_from_code = fields.CharField(max_length=12)

    country_to_code = fields.CharField(max_length=12)
    country_from_code = fields.CharField(max_length=12)

    city_from = fields.CharField(max_length=124)
    city_to = fields.CharField(max_length=124)

    distance = fields.FloatField()

    bags_price = fields.JSONField()
    bag_limit = fields.JSONField()

    availability = fields.JSONField()
    airlines = fields.JSONField()
    route = fields.JSONField()

    booking_token = fields.CharField(max_length=2048)
    deep_link = fields.CharField(max_length=2048)
    local_arrival = fields.CharField(max_length=1024)
    local_departure = fields.CharField(max_length=1024)

    price = fields.FloatField()
    price_conversion = fields.JSONField()

    response = fields.JSONField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "flights"

    @classmethod
    async def create(cls, **kwargs):
        return await super().create(**kwargs)


ModelTypes = Union[FlightsModel]
