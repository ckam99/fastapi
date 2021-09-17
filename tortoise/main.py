from fastapi import FastAPI
from models import User,Post
from database import connect_db
from schemas import UserInSchema,PostBaseSchema, UserSchema, PostSchema
from typing import List

app=FastAPI()

@app.get('/users', response_model=List[UserSchema])
async def get_users():
    return await User.all()

@app.post("/users", response_model=UserSchema)
async def create_user(payload:UserInSchema):
    user = User(**payload.dict())
    await user.save()
    return user

@app.get('/posts', response_model=List[PostSchema])
async def get_posts():
    return await Post.all()

@app.post("/posts", response_model=PostSchema)
async def create_post(payload:PostBaseSchema):
    post = Post(**payload.dict())
    await post.save()
    return post

connect_db(app)
