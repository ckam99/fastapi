from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UserBase(BaseModel):
   email: EmailStr
   name: Optional[str]
   
class UserCreate(UserBase):
   password: str

class User(UserBase):
    id:int
    # posts:List['Post']=[]
    
    class Config:
        orm_mode = True

class BasePost(BaseModel):
    title:str
    body:Optional[str]=None
    
class PostCreate(BasePost):
    user_id:Optional[int]

class Post(BasePost):
    id:int
    user:User=None
    
    class Config:
        orm_mode = True


# User.update_forward_refs()