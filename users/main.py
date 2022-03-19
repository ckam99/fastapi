from fastapi import FastAPI
from routes import router
from database import init_database

app = FastAPI()

app.include_router(router)


@app.on_event('startup')
async def startup():
    init_database(app)
    print('app started')


@app.on_event('shutdown')
async def shutdown():
    print('app started')
