from fastapi import APIRouter, Depends, BackgroundTasks, Response
from repositories.user import UserRepository
from schemas.user import UserSchema, UserInSchema
from typing import List
from tasks import user as user_task
from schemas.user import UserInSchema, UserSchema
from tasks.user import user_created

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/', response_model=List[UserSchema])
async def get_users(repository: UserRepository = Depends()):
    return await repository.fetch_all()


@router.post('/', response_model=UserSchema)
async def create_user(data: UserInSchema, background_tasks: BackgroundTasks,
                      repository: UserRepository = Depends()):
    user = await repository.create(data)
    background_tasks.add_task(user_created,  UserSchema(**user.dict()))
    return user


@router.get('/{user_id}', response_model=UserSchema)
async def get_user(user_id: int, repository: UserRepository = Depends()):
    return await repository.fetch_one(user_id)


@router.put('/{user_id}', response_model=UserSchema)
async def update_user(user_id: int, background_tasks: BackgroundTasks, repository: UserRepository = Depends()):
    user = await repository.update(user_id)
    background_tasks.add_task(user_task.user_updated,  user)
    return user


@router.delete('/{user_id}')
async def delete_user(user_id: int, background_tasks: BackgroundTasks,
                      repository: UserRepository = Depends()):
    user = await repository.remove(user_id)
    background_tasks.add_task(user_task.user_deleted, user)
    return Response(status_code=204)
