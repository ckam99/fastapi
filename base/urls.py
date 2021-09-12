from os import path
from base.services import AuthService, UserService, RoleService
from core.contrib.security import OAuth, OAuth2PasswordRequestForm
from core.contrib import view
from core.contrib.medias import upload_multiple_files, get_media
from .schemas import (RegisterSchema, RoleCredentialSchema, RoleSchema,
                      UserSchema, LoginSchema, UserTokenSchema, ConfirmEmailSchema)
from typing import List
from fastapi import Depends, Request
from . import router


@router.get('/', include_in_schema=False)
def index(request: Request):
    return view.TemplateResponse('index.html', {'request': request})


@router.post(path='/auth/register',   response_model=UserSchema, tags=['Authentication'])
async def register(payload: RegisterSchema):
    rep = await AuthService.register(payload)
    return rep


@router.post(path='/auth/login',  response_model=UserTokenSchema, tags=['Authentication'])
async def login(payload: LoginSchema):
    rep = await AuthService.login(payload)
    return rep


@router.post(path='/oauth/login',  summary="Oauth authentication", response_model=UserTokenSchema, tags=['Authentication'])
async def oauth_login(payload: OAuth2PasswordRequestForm = Depends()):
    rep = await AuthService.oauth_login(username=payload.username, password=payload.password)
    return rep


@router.get(path='/auth/me', summary="Get current user", response_model=UserSchema, tags=['Authentication'])
async def get_auth_user(user: UserSchema = Depends(OAuth.get_current_user)):
    ''' Get current user '''
    return user


@router.post(path='/auth/confirm', summary="Confirm email", response_model=UserSchema, tags=['Authentication'])
async def confirm_email(payload: ConfirmEmailSchema):
    ''' Confirm user email '''
    user = await AuthService.confirm_email(**payload.dict())


@router.get(path='/users', response_model=List[UserSchema], tags=['Users'])
async def get_users():
    ''' Get all users '''
    return await UserService.list()


@router.get(path='/users/roles', response_model=List[RoleSchema], tags=['Users'])
async def get_roles():
    '''  Get all roles '''
    return await RoleService.list()


@router.post(path='/users/roles', response_model=RoleSchema, tags=['Users'])
async def create_role(credentials: RoleCredentialSchema):
    ''' Create new role '''
    return await RoleService.create(credentials)

# @router.get('/media/{path}', tags=['Medias'], summary="Get uploaded file")
# async def get_file(*, path: str):
#     return await get_media(path)


# @router.post('/media', tags=['Medias'], summary='Upload file')
# async def upload_file(files=Depends(upload_multiple_files)):
#     return {"message": "ashdka"}
