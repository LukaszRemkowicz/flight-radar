from typing import Union

from .types import models


class FlightsModel:
    flight_to_code = models.CharField(max_length=12)
    flight_from_code = models.CharField(max_length=12)

    country_to_code = models.CharField(max_length=12)
    country_from_code = models.CharField(max_length=12)

    city_from = models.CharField(max_length=124)
    city_to = models.CharField(max_length=124)

    distance = models.FloatField()

    bags_price = models.JsonField()
    bag_limit = models.JsonField()

    availability = models.JsonField()
    airlines = models.JsonField()
    route = models.JsonField()

    booking_token = models.CharField(max_length=1024)
    deep_link = models.CharField(max_length=2048)
    local_arrival = models.CharField(max_length=1024)
    local_departure = models.CharField(max_length=1024)

    price = models.FloatField()
    price_conversion = models.JsonField()

    response = models.JsonField()
    created_at = models.DateField(auto_add=True, now=True)
    updated_at = models.DateField(now=True)


ModelTypes = Union[FlightsModel]
