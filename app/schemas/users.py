from typing import Union

from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    email: Union[str, None] = None


class CreateUserSchema(UserSchema):
    password: str


class UserLoginSchema(BaseModel):
    username: str
    password: str
