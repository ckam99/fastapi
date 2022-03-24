from fastapi import APIRouter
from . import user

router = APIRouter(prefix='/api')

router.include_router(user.router)
