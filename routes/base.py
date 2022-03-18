from fastapi import APIRouter
from . import message

router = APIRouter(prefix='/api')

router.include_router(message.router)
