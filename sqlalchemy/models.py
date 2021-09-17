import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Text, Column, Boolean, Integer, String, DateTime, ForeignKey
from database import BaseModel


class User(BaseModel):
    __tablename__ = 'users'
    
    id=Column(Integer, primary_key=True,index=True)
    name=Column(String, nullable=True)
    email=Column(String, unique=True, index=True)
    password=Column(String)
    created_at=Column(DateTime, default=datetime.datetime.utcnow)
    posts=relationship('Post', back_populates='user', cascade='all, delete-orphan')

class Post(BaseModel):
    __tablename__='posts'
    
    id=Column(Integer, primary_key=True,index=True)
    title = Column(String)
    body = Text()
    user_id = Column(Integer, ForeignKey(User.id), nullable=True)
    user = relationship("User", back_populates='posts')
