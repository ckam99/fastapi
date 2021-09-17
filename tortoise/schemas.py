from pydantic import BaseModel, EmailStr, validator
from exceptions import CustomException
from typing import Optional

class BaseUserSchema(BaseModel):
    name:str
    lastname:str
    firstname:str
    email:EmailStr
    phone:Optional[str]
    
    
class UserSchema(BaseUserSchema):
    id:int
    
    class Config:
        orm_mode=True
    

class UserInSchema(BaseUserSchema):
    password:str
    
    @validator('password')
    @classmethod
    def validate_password(cls, value):
        if len(value) < 4:
            raise CustomException(value, 'Password must be at least 4 characters')
        return value

class PostBaseSchema(BaseModel):
    title:str
    body:str
    user_id:int
    
    
class PostSchema(PostBaseSchema):
    id:int
    
    class Config:
        orm_mode=True
