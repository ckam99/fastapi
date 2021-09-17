from pydantic import BaseModel, validator
# from tortoise.contrib.pydantic import PydanticModel, pydantic_model_creator
from exceptions import CustomException
from typing import Optional, List
from datetime import datetime
# import models

# Post = pydantic_model_creator(models.Post)
# User = pydantic_model_creator(models.User)


class UserSchema(BaseModel):
    id: int
    firstname: str
    lastname: str
    # full_name: Optional[str]
    phone: Optional[str]
    created_at: datetime = None
    modified_at: datetime = None

    class Config:
        orm_mode = True


class UserInSchema(BaseModel):
    lastname: str
    firstname: str
    phone: Optional[str]
    password: str

    @validator('password')
    @classmethod
    def validate_password(cls, value):
        if len(value) < 4:
            raise CustomException(
                value, 'Password must be at least 4 characters')
        return value


class PostInSchema(BaseModel):
    title: str
    body: str
    user_id: int


class PostBaseSchema(PostInSchema):
    id: int
    created_at: datetime = None
    modified_at: datetime = None


class PostSchema(BaseModel):
    id: int
    title: str
    body: str
    user: UserSchema = None

    class Config:
        orm_mode = True


class UserPostSchema(UserSchema):
    posts: List[PostBaseSchema] = []
