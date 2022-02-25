from pydantic import BaseModel


class ValidationSchema(BaseModel):
    field: str
    type: str
    msg: str
