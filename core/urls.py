from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from auth.urls import router as auth

router = APIRouter()
router.include_router(
    auth, prefix='/auth', tags=['auth'],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},)


@router.get('/')
def index():
    return {'message': 'hello'}
