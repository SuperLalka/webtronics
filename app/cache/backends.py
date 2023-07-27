import abc
from typing import List

import aioredis


class CacheBackend(abc.ABC):
    @abc.abstractmethod
    async def get(self, key: str) -> bytes:
        raise NotImplementedError

    @abc.abstractmethod
    async def set(self, key: str, value: bytes, expire: int) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, *keys: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def keys(self, pattern: str) -> List[str]:
        raise NotImplementedError


class RedisCacheBackend(CacheBackend):
    def __init__(self, redis: aioredis.Redis):
        self._redis = redis

    async def get(self, key: str) -> bytes:
        return await self._redis.get(key)

    async def set(self, key: str, value: bytes, expire: int) -> None:
        await self._redis.set(key, value, ex=expire)

    async def delete(self, *keys: str) -> None:
        if len(keys) > 0:
            await self._redis.delete(*keys)

    async def keys(self, pattern: str) -> List[str]:
        return await self._redis.keys(pattern)
