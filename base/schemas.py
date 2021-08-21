from pydantic import BaseModel, EmailStr
from tortoise.contrib.pydantic import PydanticModel
from typing import Optional
from fastapi import UploadFile, File


class UserBaseSchema(BaseModel):
    name:  Optional[str]
    username: str
    email: EmailStr


class UserSchema(UserBaseSchema):
    id: int
    avatar: str


class UserTokenSchema(UserSchema):
    access_token: str
    token_type: Optional[str]


class RegisterSchema(UserBaseSchema):
    password: str
    # avatar: Optional[UploadFile] = File(...)


class LoginSchema(BaseModel):
    password: str
    email: EmailStr
