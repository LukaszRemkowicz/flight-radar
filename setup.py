from flight_radar.settings import get_db_credentials


AERICH_DB_CONFIG: dict = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": get_db_credentials(),
        },
    },
    "apps": {
        "models": {
            "models": ["__main__", "flight_radar.models.models", "aerich.models"],
            "default_connection": "default",
        },
    },
    "default_connection": "default",
}
