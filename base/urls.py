from os import path
from core.contrib.security import OAuth, OAuth2PasswordRequestForm
from .models import User
from .schemas import RegisterSchema, UserSchema, LoginSchema, UserTokenSchema
from typing import List
from tortoise.query_utils import Q
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi import APIRouter, Request
from core.contrib import view
from core.generics.medias import upload_multiple_files, get_media

router = APIRouter()
oauth = OAuth()


@router.get('/', include_in_schema=False)
def index(request: Request):
    return view.TemplateResponse('index.html', {'request': request})


@router.post(path='/auth/register',   response_model=UserSchema, tags=['Authentication'])
async def register(payload: RegisterSchema):
    obj = await User.filter(Q(email=payload.email) | Q(username=payload.username)).first()
    if obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Email or username already exist')
    user_obj = User(**payload.dict())
    user_obj.set_password(payload.password)
    await user_obj.save()
    return user_obj


@router.post(path='/auth/login',  response_model=UserTokenSchema, tags=['Authentication'])
async def login(payload: LoginSchema):
    user = await oauth.authenticate(payload.email, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Email or password incorrect.')
    return oauth.generate_token(dict(user))


@router.post(path='/oauth/login',  summary="Oauth authentication", response_model=UserTokenSchema, tags=['Authentication'])
async def oauth_login(payload: OAuth2PasswordRequestForm = Depends()):
    user = await oauth.authenticate(payload.username, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Email or password incorrect.')
    return oauth.generate_token(dict(user))


@router.get(path='/auth/me', summary="Get current user", response_model=UserSchema, tags=['Authentication'])
async def get_user(user: UserSchema = Depends(oauth.get_current_user)):
    return user


@router.get(path='/users', response_model=List[UserSchema], tags=['Users'])
async def get_users():
    return await User.all()


@router.get('/media/{path}', tags=['Medias'], summary="Get uploaded file")
async def get_file(*, path: str):
    return await get_media(path)


@router.post('/media', tags=['Medias'], summary='Upload file')
async def upload_file(files=Depends(upload_multiple_files)):
    return {"message": "ashdka"}
