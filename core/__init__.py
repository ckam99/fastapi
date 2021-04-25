from fastapi import FastAPI, Depends
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise
import logging
from .urls import router

app = FastAPI()

register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['auth.models']},
    generate_schemas=True,
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
