import os
import logging

import aioredis
from fastapi import FastAPI
from starlette.middleware.authentication import AuthenticationMiddleware

import authentication
import database
from app.cache.backends import RedisCacheBackend
from app.cache.middlewares import CacheMiddleware
from app.routes import router
from config import Config


logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

app = FastAPI(
    openapi_url="/documentation/openapi.json",
    redoc_url="/documentation/redoc",
    docs_url="/documentation/docs",
    debug=True
)

app.add_middleware(CacheMiddleware)
app.add_middleware(AuthenticationMiddleware, backend=authentication.BearerTokenAuthBackend())
app.add_middleware(authentication.JWTAuthSessionMiddleware)
app.add_middleware(database.DBSessionMiddleware)


@app.on_event("startup")
async def startup():
    app.include_router(router)

    redis = aioredis.from_url(
        os.getenv("REDIS_CACHE_URL", "redis://cache-redis"),
        encoding="utf8",
        decode_responses=True,
    )

    CacheMiddleware.setup(
        RedisCacheBackend(redis),
        [
            {
                "url_regex": r"^(/posts/\d+/like/?)$",
                "expire": Config.CACHE_TTL,
            },
        ],
    )


@app.on_event("shutdown")
async def shutdown():
    pass
