from dataclasses import dataclass


@dataclass
class ConfigRepo:
    """base scrapper config represents second calls between each request"""

    MIN_WAIT_BEFORE: int = 2
    MAX_WAIT_BEFORE: int = 2
    MAX_ATTEMPTS: int = 4
    MIN_WAIT_BETWEEN: int = 5
    MAX_WAIT_BETWEEN: int = 5

    async def get_config(self):
        """get config"""
        return self
