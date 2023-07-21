
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException

import authentication
import database
from app.routes import router


app = FastAPI()
app.add_middleware(database.DBSessionMiddleware)
app.add_middleware(authentication.JWTAuthSessionMiddleware)


@app.on_event("startup")
async def startup():
    app.include_router(router)


@app.on_event("shutdown")
async def shutdown():
    pass


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )
