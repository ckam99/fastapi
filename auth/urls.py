from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from tortoise.query_utils import Q
from typing import List
from .schemas import RegisterSchema, UserSchema, LoginSchema, UserTokenSchema
from .models import User
from core.contrib.security import OAuth, OAuth2PasswordRequestForm


router = APIRouter()
oauth = OAuth()


@router.post('/register',  response_model=UserSchema)
async def register(payload: RegisterSchema):
    obj = await User.filter(Q(email=payload.email) | Q(username=payload.username)).first()
    if obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Email or username already exist')
    user_obj = User(**payload.dict())
    user_obj.set_password(payload.password)
    await user_obj.save()
    return user_obj


@router.post('/login',  response_model=UserTokenSchema)
async def login(payload: OAuth2PasswordRequestForm = Depends()):
    user = await oauth.authenticate(payload.username, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Email or password incorrect.')
    return oauth.generate_token(dict(user))
    # user_obj = dict(user)
    # del user_obj['password']
    # token = jwt.encode(user_obj, SECRET_KEY)
    # user_obj['access_token'] = token
    # user_obj['token_type'] = 'bearer'
    # return user_obj


@router.get('/me', response_model=UserSchema)
async def get_user(user: UserSchema = Depends(oauth.get_current_user)):
    return user


@router.get('/users', response_model=List[UserSchema])
async def get_users():
    return await User.all()
