import json

from app.settings import settings


class Cache:
    def __init__(self, expiry: int = settings.cache_expire):
        self.cache_expiry = expiry

    async def get(self, key) -> json:
        cached_data = await settings.redis_client.get(key)

        return cached_data

    async def set(self, key, value):
        await settings.redis_client.setex(key, self.cache_expiry, value)
