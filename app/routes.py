from fastapi import APIRouter, Depends
from services import PostAPIView
from schemas import AbstractPost, Post
from typing import List
from models import Post

router = APIRouter(prefix='/api')

@router.get('/posts', response_model=List[Post])
async def get_posts(view: PostAPIView = Depends(PostAPIView)):
    return await view.all()


@router.post('/posts', response_model=Post)
async def create_post(data: AbstractPost, view: PostAPIView = Depends(PostAPIView)):
    return await view.create(data)


@router.get('/posts/{post_id}', response_model=Post)
async def get_post(post_id: int, view: PostAPIView = Depends(PostAPIView)):
    return await view.find(post_id)


@router.delete('/posts/{post_id}')
async def delete_post(post_id: int, view: PostAPIView = Depends(PostAPIView)):
    return await view.remove(post_id)