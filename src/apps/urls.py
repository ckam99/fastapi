from fastapi import APIRouter
from .base.urls import router as base_urls

router = APIRouter()

router.include_router(base_urls)
# router.include_router(
#     auth_urls,
#     responses={404: {"description": "Not found"}},
# )


@router.get('/hello')
def say_hello():
    return {'message': 'Hello everybody!'}
