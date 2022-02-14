from pydantic import BaseModel
from typing import Optional


class AbstractPost(BaseModel):
    title: str
    body: str
    image: Optional[str]


class Post(AbstractPost):
    id: int
