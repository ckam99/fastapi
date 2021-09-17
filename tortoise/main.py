from fastapi import FastAPI, Depends
from models import User, Post
from database import connect_db
import schemas
from typing import List
from views import PostAPIView, UserAPIView

app = FastAPI()


@app.get('/users',  response_model=List[schemas.UserSchema], tags=['Users'])
async def get_users(repo: UserAPIView = Depends(UserAPIView)):
    return await repo.all()


@app.post("/users", response_model=schemas.UserSchema, tags=['Users'])
async def create_user(payload: schemas.UserInSchema, repo: UserAPIView = Depends(UserAPIView)):
    return await repo.create(payload)


@app.get("/users/{user_id}", response_model=schemas.UserSchema, tags=['Users'])
async def get_user(user_id: int, repo: UserAPIView = Depends(UserAPIView)):
    return await repo.find(user_id)


@app.get('/posts', response_model=List[schemas.PostSchema], tags=['Posts'])
async def get_posts(repo: PostAPIView = Depends(PostAPIView)):
    return await repo.all()


@app.post("/posts", response_model=schemas.PostBaseSchema, tags=['Posts'])
async def create_post(payload: schemas.PostInSchema, repo: PostAPIView = Depends(PostAPIView)):
    return await repo.create(payload)


@app.get("/posts/{post_id}", response_model=schemas.PostSchema, tags=['Posts'])
async def get_post(post_id: int, repo: PostAPIView = Depends(PostAPIView)):
    return await repo.find(post_id)


@app.on_event('startup')
def on_start():
    connect_db(app)
