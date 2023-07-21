
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi_jwt_auth import AuthJWT

from app.crud.user import UserManager
from app.routes.utils import not_found
from app.schemas.auth import JWTAuthSettings
from app.schemas.users import CreateUserSchema, UserLoginSchema

router = APIRouter(prefix="/auth", tags=["auth"])


@AuthJWT.load_config
def get_config():
    return JWTAuthSettings()


@router.post('/signup')
@router.post('/signup/', include_in_schema=False)
async def signup(request: Request, data: CreateUserSchema):
    await UserManager(request.state.db_session).create(data.dict(exclude_none=True))


@router.post('/login')
@router.post('/login/', include_in_schema=False)
async def login(request: Request, data: UserLoginSchema, Authorize: AuthJWT = Depends()):
    qs = await UserManager(request.state.db_session).is_exists(data.dict())
    if not qs:
        return not_found("No user found with the specified data")

    access_token = Authorize.create_access_token(subject=data.username)
    refresh_token = Authorize.create_refresh_token(subject=data.username)

    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)
    return {"msg": "Successfully login"}


@router.post('/refresh')
@router.post('/refresh/', include_in_schema=False)
async def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)

    Authorize.set_access_cookies(new_access_token)
    return {"msg": "The token has been refresh"}


@router.delete('/logout')
@router.delete('/logout/', include_in_schema=False)
async def logout(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    Authorize.unset_jwt_cookies()
    return {"msg": "Successfully logout"}
