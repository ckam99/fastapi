from fastapi import APIRouter, Depends
from typing import List
from views.base import UserAPIView
from schemas.users import UserInSchema, UserSchema
from schemas.mixte import UserPostSchema, PostBaseSchema

router = APIRouter(tags=['Users'])


@router.get('/users',  response_model=List[UserSchema])
async def get_users(repo: UserAPIView = Depends(UserAPIView)):
    return await repo.all()


@router.post("/users", response_model=UserSchema)
async def create_user(payload: UserInSchema, repo: UserAPIView = Depends(UserAPIView)):
    return await repo.create(payload)


@router.get("/users/{user_id}", response_model=UserPostSchema)
async def get_user(user_id: int, repo: UserAPIView = Depends(UserAPIView)):
    return await repo.find(user_id)


@router.get("/users/{user_id}/posts", response_model=List[PostBaseSchema])
async def get_user_posts(user_id: int, repo: UserAPIView = Depends(UserAPIView)):
    return await repo.get_posts(user_id)
