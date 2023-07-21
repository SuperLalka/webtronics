
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import MissingTokenError
from starlette.middleware.base import BaseHTTPMiddleware

from app.routes.utils import unauthorized


class JWTAuthSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if not request.url.path.startswith("/auth/"):
            try:
                Authorize = AuthJWT(request)
                Authorize.jwt_required()
            except MissingTokenError:
                return unauthorized()
        return await call_next(request)
