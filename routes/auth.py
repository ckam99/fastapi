from views.auth import AuthAPIView
from core.security import OAuth, OAuth2PasswordRequestForm
from schemas.auth import (
    RegisterSchema,
    UserSchema,
    LoginSchema,
    UserTokenSchema,
    ConfirmEmailSchema
)
from fastapi import Depends, APIRouter
from core.validators import UserValidator

router = APIRouter(prefix='/auth')


@router.post(path='/register',   response_model=UserSchema, tags=['Authentication'])
async def register(credentials: RegisterSchema, repo: AuthAPIView = Depends(), validator: UserValidator = Depends()):
    await validator.validate_unique_fields(**credentials.dict())
    return await repo.register(credentials)


@router.post(path='/login',  response_model=UserTokenSchema, tags=['Authentication'])
async def login(credentials: LoginSchema, repo: AuthAPIView = Depends()):
    return await repo.login(credentials)


@router.post(path='/oauth/login',  summary="Oauth authentication", response_model=UserTokenSchema, tags=['Authentication'])
async def oauth_login(credentials: OAuth2PasswordRequestForm = Depends(), repo: AuthAPIView = Depends()):
    return await repo.oauth_login(username=credentials.username, password=credentials.password)


@router.get(path='/me', summary="Get current user", response_model=UserSchema, tags=['Authentication'])
async def get_auth_user(user: UserSchema = Depends(OAuth.get_current_user)):
    ''' Get current user '''
    return user


@router.post(path='/confirm', summary="Confirm email", response_model=UserSchema, tags=['Authentication'])
async def confirm_email(credentials: ConfirmEmailSchema, repo: AuthAPIView = Depends()):
    ''' Confirm user email '''
    return await repo.confirm_email(**credentials.dict())


# @router.post('/media', tags=['Medias'], summary='Upload file')
# async def upload_file(files=Depends(upload_multiple_files)):
#     return {"message": "ashdka"}
