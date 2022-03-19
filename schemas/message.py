from pydantic import BaseModel


class Message(BaseModel):
    id: int
    message: str


class MessageIn(BaseModel):
    message: str
