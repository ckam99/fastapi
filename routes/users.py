from fastapi import APIRouter, Depends
from typing import List
from views.users import UserAPIView
from views.auth import RoleAPIView
from schemas.auth import RegisterSchema, UserSchema, RoleSchema, RoleInSchema
from schemas.mixte import UserPostSchema, PostBaseSchema

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/',  response_model=List[UserSchema])
async def get_users(repo: UserAPIView = Depends(UserAPIView)):
    return await repo.all()


@router.post('/', response_model=UserSchema)
async def create_user(credentials: RegisterSchema, repo: UserAPIView = Depends(UserAPIView)):
    return await repo.create(credentials)


@router.get('/{user_id}', response_model=UserPostSchema)
async def get_user(user_id: int, repo: UserAPIView = Depends(UserAPIView)):
    return await repo.find(user_id)


@router.get('/{user_id}/posts', response_model=List[PostBaseSchema])
async def get_user_posts(user_id: int, repo: UserAPIView = Depends(UserAPIView)):
    return await repo.get_posts(user_id)


@router.get(path='/roles', response_model=List[RoleSchema], tags=['Users'])
async def get_roles(repo: RoleAPIView = Depends()):
    '''  Get all roles '''
    return await repo.list()


@router.post(path='/roles', response_model=RoleSchema, tags=['Users'])
async def create_role(credentials: RoleInSchema, repo: RoleAPIView = Depends()):
    ''' Create new role '''
    return await repo.create(credentials)
