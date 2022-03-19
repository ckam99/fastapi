from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from core.exceptions import ModelNotfoundError
from core.database import connect_database
from core.logging import register_logs
from core.helpers import register_signals
from routes.base import router


app = FastAPI()

app.include_router(router)

logger = register_logs(app)


@app.middleware("http")
async def exception_handling(request: Request, call_next):
    request.app.logger.info(f"new {request.method} request")
    try:
        return await call_next(request)
    except ModelNotfoundError as exc:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={'reason': str(exc)})


@app.on_event('startup')
async def startup():
    connect_database(app)
    register_signals()
    print('app started...')


@app.on_event('shutdown')
async def shutdown():
    print('app shutdown...')
