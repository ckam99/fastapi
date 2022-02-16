from fastapi import APIRouter, Depends, BackgroundTasks, Response
from services import PostAPIView
from schemas import AbstractPost, Post
from typing import List
from tasks import post_event


router = APIRouter(prefix='/api')


@router.get('/posts', response_model=List[Post])
async def get_posts(view: PostAPIView = Depends(PostAPIView)):
    return await view.all()


@router.post('/posts', response_model=Post)
async def create_post(data: AbstractPost, background_tasks: BackgroundTasks, view: PostAPIView = Depends(PostAPIView)):
    post = await view.create(data)
    background_tasks.add_task(post_event, 'post_created', post.dict())
    return post


@router.get('/posts/{post_id}', response_model=Post)
async def get_post(post_id: int, view: PostAPIView = Depends(PostAPIView)):
    return await view.find(post_id)


@router.delete('/posts/{post_id}')
async def delete_post(post_id: int, background_tasks: BackgroundTasks,  view: PostAPIView = Depends(PostAPIView)):
    post = await view.remove(post_id)
    background_tasks.add_task(post_event, 'post_deleted', post)
    return Response(status_code=204)
