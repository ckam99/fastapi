from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise
import logging
from base.urls import router
from . import settings


app = FastAPI(title=settings.APP_NAME)
app.mount('/static', StaticFiles(directory=settings.STATIC_DIR),
          name='static')
register_tortoise(
    app,
    config=settings.TORTOISE_ORM,
    generate_schemas=False,
    add_exception_handlers=True
)
app.include_router(router)


@app.on_event('startup')
async def onstartup():
    logging.info('Tortoise-ORM started, %s, %s',
                 Tortoise._connections, Tortoise.apps)


@app.on_event('shutdown')
async def onshutdown():
    await Tortoise.close_connections()
    logging.info('Tortoise-ORM shutting down.')
