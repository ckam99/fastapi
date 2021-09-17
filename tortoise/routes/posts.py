from __future__ import annotations
from fastapi import APIRouter, Depends
from typing import List
from views.base import PostAPIView
from schemas.posts import PostSchema, PostInSchema, PostBaseSchema

router = APIRouter(tags=['Posts'])


@router.get('/posts', response_model=List[PostSchema])
async def get_posts(repo: PostAPIView = Depends(PostAPIView)):
    return await repo.all()


@router.post("/posts", response_model=PostBaseSchema)
async def create_post(payload: PostInSchema, repo: PostAPIView = Depends(PostAPIView)):
    return await repo.create(payload)


@router.get("/posts/{post_id}", response_model=PostSchema)
async def get_post(post_id: int, repo: PostAPIView = Depends(PostAPIView)):
    return await repo.find(post_id)
