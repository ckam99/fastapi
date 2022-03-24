from pydantic import BaseModel
from datetime import datetime


class BaseSchema(BaseModel):

    class Config:
        json_encoders = {
            datetime: lambda d: d.isoformat()
        }
