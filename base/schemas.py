from pydantic import BaseModel, EmailStr
from tortoise.contrib.pydantic import PydanticModel
from typing import Optional
from fastapi import UploadFile, File
from datetime import datetime


class UserBaseSchema(BaseModel):
    name:  Optional[str]
    username: str
    email: EmailStr


class UserSchema(UserBaseSchema):
    id: int
    avatar: Optional[str]


class UserTokenSchema(UserSchema):
    access_token: str
    token_type: Optional[str]


class RegisterSchema(UserBaseSchema):
    password: str
    # avatar: Optional[UploadFile] = File(...)


class LoginSchema(BaseModel):
    password: str
    email: EmailStr


class RoleCredentialSchema(BaseModel):
    name: str


class RoleSchema(BaseModel):
    id: int
    name: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
