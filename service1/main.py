from fastapi import FastAPI
from tortoise import Tortoise
from routes import router
from settings import TORTOISE_ORM_CONFIG

app = FastAPI()


@app.on_event('startup')
async def on_start():
    await Tortoise.init(
        # db_url='sqlite://db.sqlite3',
        # modules={'models': ['models']}
        config=TORTOISE_ORM_CONFIG
    )
    await Tortoise.generate_schemas()
    print('database connected')


@app.on_event('shutdown')
async def onshutdown():
    await Tortoise.close_connections()
    print('Tortoise-ORM shutting down.')

app.include_router(router)
