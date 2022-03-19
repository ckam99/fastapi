from turtle import title
from pydantic import BaseModel
from typing import Optional


class Post(BaseModel):
    id: Optional[int]
    title: str
    body: Optional[str]
