from base.views import AuthAPIView, UserAPIView
from core.contrib.security import OAuth, OAuth2PasswordRequestForm
from core.contrib import view
from core.contrib.medias import upload_multiple_files, get_media
from .schemas import RegisterSchema, UserSchema, LoginSchema, UserTokenSchema
from typing import List
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, Request


router = APIRouter()
oauth = OAuth()

auth = AuthAPIView()
users = UserAPIView()


@router.get('/', include_in_schema=False)
def index(request: Request):
    return view.TemplateResponse('index.html', {'request': request})


@router.post(path='/auth/register',   response_model=UserSchema, tags=['Authentication'])
async def register(payload: RegisterSchema):
    rep = await auth.register(payload)
    return rep


@router.post(path='/auth/login',  response_model=UserTokenSchema, tags=['Authentication'])
async def login(payload: LoginSchema):
    rep = await auth.login(payload)
    return rep


@router.post(path='/oauth/login',  summary="Oauth authentication", response_model=UserTokenSchema, tags=['Authentication'])
async def oauth_login(payload: OAuth2PasswordRequestForm = Depends()):
    rep = await auth.oauth_login(username=payload.username, password=payload.password)
    return rep


@router.get(path='/auth/me', summary="Get current user", response_model=UserSchema, tags=['Authentication'])
async def get_auth_user(user: UserSchema = Depends(oauth.get_current_user)):
    return user


@router.get(path='/users', response_model=List[UserSchema], tags=['Users'])
async def get_users():
    return await users.list()


@router.get('/media/{path}', tags=['Medias'], summary="Get uploaded file")
async def get_file(*, path: str):
    return await get_media(path)


@router.post('/media', tags=['Medias'], summary='Upload file')
async def upload_file(files=Depends(upload_multiple_files)):
    return {"message": "ashdka"}
