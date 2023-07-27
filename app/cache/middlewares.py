import re
import logging
from typing import List, Optional, TypedDict

from fastapi import Request, Response
from fastapi.responses import ORJSONResponse
from orjson import orjson
from starlette import status
from starlette.concurrency import iterate_in_threadpool
from starlette.middleware.base import RequestResponseEndpoint, BaseHTTPMiddleware
from starlette.responses import StreamingResponse

from app.cache.backends import CacheBackend


logger = logging.getLogger(__name__)


class Resource(TypedDict):
    url_regex: str
    expire: int


class CacheMiddleware(BaseHTTPMiddleware):
    _cache_resources: List[Resource] = []
    _cache_backend: Optional[CacheBackend] = None

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if self._cache_backend is None or self._cache_resources is None:
            raise AttributeError("You must call 'setup' method before!")

        response = await call_next(request)

        if request.method.lower() != "get":
            return response

        request_url = request.url.path if not request.url.query \
            else f"{request.url.path}?{request.url.query}"
        resource = self._get_resource(request_url)

        if resource is None:
            return response

        cached_body = await self._cache_backend.get(request_url)

        if cached_body:
            logger.info(f"Response for {resource['url_regex']} is taken from cache base")
            return ORJSONResponse(status_code=200, content=orjson.loads(cached_body))

        if response.status_code == status.HTTP_200_OK:
            body = await self._get_body_from_response(response)
            await self._cache_backend.set(
                key=request_url,
                value=body,
                expire=resource["expire"],
            )
            logger.info(f"Response for {resource['url_regex']} is placed in the cache base")

        return response

    @classmethod
    def setup(cls, cache_backend: CacheBackend, cache_resources: List[Resource]) -> None:
        cls._cache_resources = cache_resources
        logger.debug("CacheMiddleware resources successfully set")
        cls._cache_backend = cache_backend
        logger.debug("CacheMiddleware backend provider (redis) successfully initialized")

    @classmethod
    async def invalidate_cache(cls, pattern: str) -> None:
        if cls._cache_backend is None:
            raise AttributeError("You must call 'setup' method before")

        cache_keys = await cls._cache_backend.keys(pattern)
        await cls._cache_backend.delete(*cache_keys)

    def _get_resource(self, request_path: str) -> Optional[Resource]:
        for resource in self._cache_resources:
            if bool(re.search(resource["url_regex"], request_path)):
                return resource
        return None

    @staticmethod
    async def _get_body_from_response(response: Response) -> bytes:
        if isinstance(response, StreamingResponse):
            response_body = [section async for section in response.body_iterator]
            response.body_iterator = iterate_in_threadpool(iter(response_body))
            return b"".join(response_body)
        return response.body
