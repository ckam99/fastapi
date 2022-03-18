from pydantic import BaseModel


class BaseMessage(BaseModel):
    message: str


class Message(BaseMessage):
    id: int
