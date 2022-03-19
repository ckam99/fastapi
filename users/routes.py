from fastapi import APIRouter, HTTPException, BackgroundTasks
from schemas import User as UserSchema
from models import User
from tortoise.contrib.pydantic import pydantic_model_creator
from tasks import user_create_task, user_remove_task, user_update_task

router = APIRouter(prefix='/users')

serializer = pydantic_model_creator(User)


@router.get('/', response_model=list[UserSchema])
async def get_users():
    return await serializer.from_queryset(User.all())


@router.get('/{user_id}')
async def get_user(user_id: int):
    obj = await User.get(id=user_id)
    if obj:
        return await serializer.from_queryset_single(obj)
    raise HTTPException(
        404, detail={'error': f'Model not found with id ({user_id})'})


@router.post('/', response_model=UserSchema)
async def create_user(user: UserSchema, btasks: BackgroundTasks):
    obj = await User.create(**user.dict(exclude={'id'}))
    obj = serializer.from_orm(obj)
    btasks.add_task(user_create_task, obj.dict())
    return obj


@router.put('/{user_id}', response_model=UserSchema)
async def update_user(user_id: int, user: UserSchema, btasks: BackgroundTasks):
    obj = await User.get(id=user_id)
    if obj:
        obj = await obj.update_from_dict(**user.dict())
        obj = await serializer.from_queryset_single(obj)
        btasks.add_task(user_update_task, obj.dict())
        return obj
    raise HTTPException(
        404, detail={'error': f'Model not found with id ({user_id})'})


@router.delete('/{user_id}')
async def delete_user(user_id: int, btasks: BackgroundTasks):
    obj = await User.get(id=user_id)
    if obj:
        await obj.delete()
        obj = await serializer.from_queryset_single(obj)
        btasks.add_task(user_remove_task, obj.dict())
    raise HTTPException(
        404, detail={'error': f'Model not found with id ({user_id})'})
