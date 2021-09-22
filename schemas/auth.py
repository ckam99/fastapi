from pydantic import BaseModel, EmailStr, validator, ValidationError
from typing import Optional
# from fastapi import UploadFile, File
from datetime import datetime
from fastapi.responses import JSONResponse
from core.schemas import ValidationSchema


class UserBaseSchema(BaseModel):
    lastname:  Optional[str]
    firstname:  Optional[str]
    username: int
    email: int
    phone: Optional[str]


class RegisterSchema(UserBaseSchema):
    password: str
    # avatar: Optional[UploadFile] = File(...)

    @validator('password')
    @classmethod
    def validate_password(cls, value):
        if len(value) < 4:
            raise JSONResponse(
                status_code=422,
                content={'errors': ValidationSchema(
                    field='password', type='type_error', msg='Password must be at least 4 characters')})
        return value


class UserSchema(UserBaseSchema):
    id: int
    avatar: Optional[str]
    created_at: datetime = None
    modified_at: datetime = None

    class Config:
        orm_mode = True


class UserTokenSchema(UserSchema):
    access_token: str
    token_type: Optional[str]
    token_expire_at: Optional[datetime]


class LoginSchema(BaseModel):
    password: str
    email: EmailStr


class RoleInSchema(BaseModel):
    name: str


class RoleSchema(BaseModel):
    id: int
    name: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class ConfirmEmailSchema(BaseModel):
    code: str
    email: EmailStr
