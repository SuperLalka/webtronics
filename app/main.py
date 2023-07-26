
from fastapi import FastAPI
from starlette.middleware.authentication import AuthenticationMiddleware

import authentication
import database
from app.routes import router

app = FastAPI(
    openapi_url="/documentation/openapi.json",
    redoc_url="/documentation/redoc",
    docs_url="/documentation/docs",
)
app.add_middleware(AuthenticationMiddleware, backend=authentication.BearerTokenAuthBackend())
app.add_middleware(authentication.JWTAuthSessionMiddleware)
app.add_middleware(database.DBSessionMiddleware)


@app.on_event("startup")
async def startup():
    app.include_router(router)


@app.on_event("shutdown")
async def shutdown():
    pass
