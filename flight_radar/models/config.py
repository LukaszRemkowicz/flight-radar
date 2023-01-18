class ConfigRepo:
    min_wait_before = 2
    max_wait_before = 2
    max_attempts = 4
    min_wait_between = 5
    max_wait_between = 5

    async def get_config(self):
        return self
