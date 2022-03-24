from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserSchema(BaseModel):
    id: int
    lastname:  Optional[str]
    firstname:  Optional[str]
    email: EmailStr
    phone: Optional[str]
    is_actif: bool
    email_confirmed_at: datetime = None
    created_at: datetime = None
    modified_at: datetime = None


class NotificationSchema(BaseModel):
    id: int
    title: str
    source: str
    body: str
    status: str
    created_at: str
    updated_at: str
    user: UserSchema = None


class NotificationInSchema(BaseModel):
    title: str
    source: str
    body: str
