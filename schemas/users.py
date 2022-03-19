from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional
from datetime import datetime


class UserBaseSchema(BaseModel):
    lastname:  Optional[str]
    firstname:  Optional[str]
    username: str
    email: EmailStr
    phone: Optional[str]


class PasswordSchema(BaseModel):
    password: str = Field(..., min_length=4,
                          description='Password must be at least 4 characters')
    password2: str

    @validator('password')
    def check_valid_password(cls, value):
        if not (any(a for a in value if str(a).isalpha())
                and any(a for a in value if str(a).isdigit())):
            raise ValueError(
                'Password must contain at least character and number')
        elif not any([s for s in '#$(&}?!{;@)*%' if s in value]):
            raise ValueError(
                'Password must contain at least special character')
        elif value.islower() or value.isupper():
            raise ValueError(
                'Password must contain at least lower and upper character')
        else:
            return value

    @validator('password2')
    def check_passwords_matching(cls, value, values):
        if 'password' in values and value != values['password']:
            raise ValueError('Passwords do not match')
        return value


class RegisterSchema(UserBaseSchema, PasswordSchema):
    pass


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
