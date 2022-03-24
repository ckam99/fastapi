from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from schemas.base import BaseSchema


class UserSchema(BaseSchema):
    id: int
    lastname:  Optional[str]
    firstname:  Optional[str]
    email: EmailStr
    is_actif: bool
    email_confirmed_at: datetime = None
    created_at: datetime = None
    modified_at: datetime = None


class UserInSchema(BaseModel):
    lastname:  Optional[str]
    firstname:  str
    email: EmailStr


class NotificationSchema(BaseSchema):
    id: int
    title: str
    source: str
    body: str
    status: str
    created_at: datetime = None
    updated_at: datetime = None
    user: UserSchema = None
