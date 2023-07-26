import jwt
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from starlette.authentication import AuthenticationBackend
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import Config
from app.crud.user import UserManager
from app.database import async_session
from app.routes.utils import unauthorized


class JWTAuthSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if not request.url.path.startswith("/auth/"):
            try:
                Authorize = AuthJWT(request)
                Authorize.jwt_required()
            except AuthJWTException:
                return unauthorized()

        return await call_next(request)


class BearerTokenAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        token = request.cookies.get("access_token_cookie")
        if not token:
            return

        try:
            decoded = jwt.decode(
                token,
                Config.AUTHJWT_SECRET_KEY,
                algorithms=[Config.AUTHJWT_ALGORITHM],
            )
            username = decoded.get("sub")

            async with async_session() as session:
                async with session.begin():
                    user = await UserManager(session).get_by_name(
                        item_username=username
                    )
            return token, user

        except Exception:
            return
