from schemas.auth import UserSchema
from schemas.posts import PostBaseSchema
from typing import List
# from pydantic import BaseModel


class UserPostSchema(UserSchema):
    id: int
    posts: List[PostBaseSchema] = []

    class Config:
        orm_mode = True
