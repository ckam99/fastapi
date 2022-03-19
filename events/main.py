from fastapi import FastAPI
from .database import init_database


app = FastAPI()


@app.on_event('startup')
async def startup():
    init_database(app)
    print('app started')


@app.on_event('shutdown')
async def shutdown():
    print('app started')
