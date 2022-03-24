from fastapi import APIRouter
from . import notification

router = APIRouter(prefix='/api')

router.include_router(notification.router)
