from fastapi import APIRouter

router = APIRouter()


@router.on_event('startup')
def on_start():
    from . import signals
    print('base app is started....')
