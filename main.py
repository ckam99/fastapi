from fastapi import FastAPI, Request, status
from core.exceptions import (
    BadCredentialsError,
    ModelNotfoundError,
    TokenInvalidError,
    TokenExpirateError,
    UnAuthorizedError
)
from routes.base import router
from database.base import connect_db
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from core.utils import format_validation_errors
from core.middlewares import register_cors
from core.logging import register_logs
from core.utils import register_signals

app = FastAPI()
app.mount('/static', StaticFiles(directory='resources/static'),
          name='static')
logger = register_logs(app)


@app.on_event('startup')
async def on_start():
    logger.info('App started ...')
    register_cors(app)
    register_signals()


@app.on_event('shutdown')
async def on_shutdown():
    logger.info('app shut down...')

connect_db(app)
app.include_router(router)


@app.middleware("http")
async def errors_handling(request: Request, call_next):
    try:
        return await call_next(request)
    except (BadCredentialsError, ) as exc:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={'reason': str(exc)})
    except ModelNotfoundError as exc:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={'reason': str(exc)})
    except (TokenExpirateError, TokenInvalidError) as exc:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                            content={'reason': str(exc)})
    except UnAuthorizedError as exc:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={'reason': str(exc)},
                            headers={"WWW-Authenticate": "Bearer"},)
    # except Exception as ex:
    #     print(ex)
    #     return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #                         content={'reason': "Contact your developeur!"})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "errors":  format_validation_errors(exc.errors())},
    )
