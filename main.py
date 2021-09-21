from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from core.database import connect_db, Tortoise
from core.middlewares import register_cors
from routes import users, auth
from core.views import render
# from core.generic.medias import upload_multiple_files, get_media


app = FastAPI()

app.mount('/static', StaticFiles(directory='resources/static'),
          name='static')

app.include_router(auth.router)
app.include_router(users.router)


@app.get('/', include_in_schema=False)
def home(request: Request):
    return render(request, 'index.html')


# @router.get('/media/{path}', tags=['Medias'], summary="Get uploaded file")
# async def get_file(*, path: str):
#     return await get_media(path)

@app.on_event('startup')
def on_start():
    connect_db(app)
    register_cors(app)


@app.on_event('shutdown')
async def onshutdown():
    await Tortoise.close_connections()
    print('Tortoise-ORM shutting down.')
