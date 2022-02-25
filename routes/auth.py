from fastapi import APIRouter, Depends
from schemas import users as schemas
from repositories.users import AuthRepository
from database.helpers import get_current_user


router = APIRouter()


@router.post(path='/register',   response_model=schemas.UserSchema)
async def register(credentials: schemas.RegisterSchema, repo: AuthRepository = Depends()):
    ''' Registration '''
    return await repo.register(credentials)


@router.post(path='/login',  response_model=schemas.UserTokenSchema)
async def login(credentials: schemas.LoginSchema, repo: AuthRepository = Depends()):
    ''' Authentication '''
    return await repo.login(credentials)


@router.get(path='/me', summary="Get current user", response_model=schemas.UserSchema)
async def get_auth_user(user: schemas.UserSchema = Depends(get_current_user)):
    ''' Get current user '''
    return user


@router.post(path='/confirm', summary="Confirm email", response_model=schemas.UserSchema)
async def confirm_email(credentials: schemas.ConfirmEmailSchema, repo: AuthRepository = Depends()):
    ''' Confirm user email '''
    return await repo.confirm_email(**credentials.dict())
