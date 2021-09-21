from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from core.database.core import connect_db, Tortoise
from core.middlewares import register_cors
from apps.urls import router
from . import settings


app = FastAPI(title=settings.APP_NAME)
app.mount('/static', StaticFiles(directory=settings.STATIC_DIR),
          name='static')

app.include_router(router)


@app.on_event('startup')
async def onstartup():
    await connect_db(app)
    register_cors(app)


@app.on_event('shutdown')
async def onshutdown():
    await Tortoise.close_connections()
    logging.info('Tortoise-ORM shutting down.')
