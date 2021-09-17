from pydantic import BaseModel
from datetime import datetime
from schemas.users import UserSchema


class PostInSchema(BaseModel):
    title: str
    body: str
    user_id: int


class PostBaseSchema(PostInSchema):
    id: int
    created_at: datetime = None
    modified_at: datetime = None

    class Config:
        orm_mode = True


class PostSchema(BaseModel):
    id: int
    title: str
    body: str
    user: UserSchema = None

    class Config:
        orm_mode = True
