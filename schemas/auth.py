from pydantic import BaseModel, EmailStr, validator
from typing import Optional
# from fastapi import UploadFile, File
from core.exceptions import ValidationException
from datetime import datetime
from core.utils import email_exists, phone_exists
from fastapi import HTTPException


class UserBaseSchema(BaseModel):
    lastname:  Optional[str]
    firstname:  Optional[str]
    username: str
    email: EmailStr
    phone: Optional[str]


class RegisterSchema(UserBaseSchema):
    password: str
    # avatar: Optional[UploadFile] = File(...)

    @validator('password')
    @classmethod
    def validate_password(cls, value):
        if len(value) < 4:
            raise HTTPException(422, 'Password must be at least 4 characters')
        return value

    @validator('email')
    @classmethod
    def validate_email(cls, value):
        exist = email_exists(value)
        print('exist email=', exist)
        if exist:
            raise HTTPException(422, 'Email is not available')
        return value

    @validator('phone')
    @classmethod
    def validate_phone(cls, value):
        if value is not None and phone_exists(value):
            print('exist phone=', True)
            raise HTTPException(422, 'Phone is not available')
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
