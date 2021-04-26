from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise
import logging
from .urls import router
from .generics.medias import upload_multiple_files, get_media
from .settings import STATIC_DIR


app = FastAPI()
app.mount('/static', StaticFiles(directory=STATIC_DIR), name=STATIC_DIR)
register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['auth.models']},
    generate_schemas=True,
    add_exception_handlers=True
)
app.include_router(router)

# = Path(..., regex='(?:[^\/]*+)$(?<=\..)')


@app.get('/media/{path}')
async def get_file(*, path: str):
    return await get_media(path)


@app.post('/media')
async def upload_file(files=Depends(upload_multiple_files)):
    return {"message": "ashdka"}


@app.on_event('startup')
async def onstartup():
    logging.info('Tortoise-ORM started, %s, %s',
                 Tortoise._connections, Tortoise.apps)


@app.on_event('shutdown')
async def onshutdown():
    await Tortoise.close_connections()
    logging.info('Tortoise-ORM shutting down.')
