from fastapi import FastAPI
from core.database import connect_db
from routes import router

app = FastAPI()


@app.on_event('startup')
async def on_start():
    print('started')


@app.on_event('shutdown')
async def onshutdown():
    print("shut down")


connect_db(app)
app.include_router(router)
