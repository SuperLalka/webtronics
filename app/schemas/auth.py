import os

from pydantic import BaseModel

from app.config import Config


class JWTAuthSettings(BaseModel):
    authjwt_secret_key: str = Config.AUTHJWT_SECRET_KEY
    authjwt_algorithm: str = Config.AUTHJWT_ALGORITHM
    authjwt_access_token_expires: int = Config.AUTHJWT_ACCESS_TOKEN_EXPIRE
    authjwt_refresh_token_expires: int = Config.AUTHJWT_REFRESH_TOKEN_EXPIRE
    authjwt_token_location: set = Config.AUTHJWT_TOKEN_LOCATION
    authjwt_cookie_csrf_protect: bool = Config.AUTHJWT_COOKIE_CSRF_PROTECT


class UserTokenSchema(BaseModel):
    access_token: str
    token_type: str
