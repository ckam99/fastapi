from fastapi import APIRouter
from . import event

router = APIRouter(prefix='/api')

router.include_router(event.router)
