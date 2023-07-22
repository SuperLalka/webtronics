import requests
from typing import Union

from pydantic import BaseModel, validator

from app.config import Config
from app.logger import logger


class UserSchema(BaseModel):
    username: str
    email: Union[str, None] = None


class CreateUserSchema(UserSchema):
    password: str

    @validator("email", pre=True)
    def validate_email(cls, value):
        params = {
            "email": value,
            "api_key": Config.EMAIL_HUNTER_API_KEY
        }
        rsp = requests.get(url=Config.EMAIL_HUNTER_API_VERIFY, params=params)

        if rsp.status_code != 200:
            logger.warning("Request to email verification service failed")
        else:
            rsp_data = rsp.json()
            if rsp_data["data"]["status"] == "invalid":
                raise ValueError("The email address is not valid")

        return value


class UserLoginSchema(BaseModel):
    username: str
    password: str
