from pydantic import BaseModel
from typing import Optional
from datetime import datetime


def datetime_str(dt: datetime) -> str:
    return dt.isoformat()


class User(BaseModel):
    id: Optional[int]
    email: str
    name: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        json_encoders = {
            datetime: datetime_str
        }
