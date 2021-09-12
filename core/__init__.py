from fastapi import FastAPI
from . import settings
from .router import router
from .config.database import engine
from sqlmodel import SQLModel
from fastapi.staticfiles import StaticFiles


def include_router(app):
    app.include_router(router)


def configure_static(app):
    app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")


def generate_database():
    SQLModel.metadata.create_all(engine)
    print('Database successfully created')


def start_application():
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=settings.APP_DESCRIPTION,
        contact={"name": settings.APP_NAME,
                 "email": "contact@example.com"},
    )
    include_router(app)
    configure_static(app)
    return app


app = start_application()


@app.on_event("startup")
def on_startup():
    generate_database()
