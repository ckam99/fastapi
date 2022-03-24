from schemas.base import BaseModel, BaseSchema
from typing import Optional
from datetime import datetime


class EventSchema(BaseSchema):
    id: int
    title: str
    source: str
    descrition: Optional[str]
    payload: Optional[dict] = None
    created_at: Optional[datetime] = None
    updated_at:   Optional[datetime] = None

    class Config:
        json_encoders = {
            datetime: lambda d: d.isoformat()
        }


class EventInSchema(BaseModel):
    title: str
    source: str
    descrition: Optional[str]
    payload: dict
