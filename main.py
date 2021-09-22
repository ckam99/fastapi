from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from core.database import connect_db, Tortoise
from core.middlewares import register_cors
# from core.exceptions import RegisterExceptionRoute

from routes import users, auth
from core.views import render
# from core.generic.medias import upload_multiple_files, get_media

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from core.utils import format_validation_errors

app = FastAPI()

app.mount('/static', StaticFiles(directory='resources/static'),
          name='static')

app.include_router(auth.router)
app.include_router(users.router)
# app.router.route_class = RegisterExceptionRoute


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "errors":  format_validation_errors(exc.errors())},
    )


@app.get('/', include_in_schema=False, )
def home(request: Request):
    return render(request, 'index.html')


# @router.get('/media/{path}', tags=['Medias'], summary="Get uploaded file")
# async def get_file(*, path: str):
#     return await get_media(path)

@ app.on_event('startup')
def on_start():
    connect_db(app)
    register_cors(app)


@ app.on_event('shutdown')
async def onshutdown():
    await Tortoise.close_connections()
    print('Tortoise-ORM shutting down.')
