from pydantic import BaseModel, validator
from generics.exceptions import CustomException
from typing import Optional
from datetime import datetime


class UserSchema(BaseModel):
    id: int
    firstname: str
    lastname: str
    # full_name: Optional[str]
    phone: Optional[str]
    created_at: datetime = None
    modified_at: datetime = None

    class Config:
        orm_mode = True


class UserInSchema(BaseModel):
    lastname: str
    firstname: str
    phone: Optional[str]
    password: str

    @validator('password')
    @classmethod
    def validate_password(cls, value):
        if len(value) < 4:
            raise CustomException(
                value, 'Password must be at least 4 characters')
        return value
