from schemas.users import UserSchema
from schemas.posts import PostBaseSchema
from typing import List, Any
from pydantic import BaseModel


class UserPostSchema(UserSchema):
    id: int
    posts: List[PostBaseSchema] = []

    class Config:
        orm_mode = True
