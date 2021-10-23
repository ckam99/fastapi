from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    firstname: Optional[str]
    lastname: Optional[str]
    email: str
    password: Optional[str]


class Post(BaseModel):
    title: str
    body: str
    user_id: Optional[int]
