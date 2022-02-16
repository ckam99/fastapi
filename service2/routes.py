from fastapi import APIRouter, Depends, BackgroundTasks, Response
from views import PostAPIView
from schemas import Post
from typing import List


router = APIRouter()


@router.get('/posts', response_model=List[Post])
async def get_posts(view: PostAPIView = Depends(PostAPIView)):
    return await view.all()


@router.get('/posts/{post_id}', response_model=Post)
async def get_post(post_id: int, view: PostAPIView = Depends(PostAPIView)):
    return await view.find(post_id)
