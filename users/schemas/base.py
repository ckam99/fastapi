from pydantic import BaseModel
from datetime import datetime


def datetime_str(dt: datetime) -> str:
    return dt.isoformat()


class BaseSchema(BaseModel):

    class Config:
        json_encoders = {
            datetime: datetime_str
        }
