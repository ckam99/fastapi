from pydantic import BaseModel
from tortoise.contrib.pydantic import PydanticModel
from typing import Optional


class UserBaseSchema(BaseModel):
    name:  Optional[str]
    username: str
    email: str


class UserSchema(UserBaseSchema):
    id: int


class UserTokenSchema(UserSchema):
    access_token: str
    token_type: Optional[str]


class RegisterSchema(UserBaseSchema):
    password: str


class LoginSchema(BaseModel):
    password: str
    email: str
