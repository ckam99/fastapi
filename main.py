from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise
import logging
from router import router


app = FastAPI()

register_tortoise(
    app,
    db_url="sqlite://database.db",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

app.include_router(router)


@app.on_event('startup')
async def onstartup():
    await Tortoise.generate_schemas()
    logging.info('Tortoise-ORM started, %s, %s',
                 Tortoise._connections, Tortoise.apps)


@app.on_event('shutdown')
async def onshutdown():
    await Tortoise.close_connections()
    logging.info('Tortoise-ORM shutting down.')
