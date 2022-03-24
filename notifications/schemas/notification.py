from schemas.base import BaseSchema, BaseModel
from typing import Optional
from datetime import datetime
from models.notification import NotificationStatus


class NotificationSchema(BaseSchema):
    id: int
    title: str
    source: str
    descrition: Optional[str]
    body: dict = None
    status: Optional[NotificationStatus]
    created_at: datetime = None
    updated_at: datetime = None
    user_id: int

    # class Config:
    #     use_enum_values = True


class NotificationInSchema(BaseModel):
    title: str
    source: str
    descrition: Optional[str]
    body: dict
    user_id: int
