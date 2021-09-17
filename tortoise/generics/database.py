from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise
from fastapi import FastAPI
import settings


def connect_db(app: FastAPI):
    register_tortoise(
        app,
        db_url=settings.DATABASE_URL,
        modules={"models": settings.DATABASE_REGISTER_MODELS},
        generate_schemas=settings.DATABASE_GENERATE_SCHEMAS,
        add_exception_handlers=True,
    )
    if settings.DATABASE_GENERATE_SCHEMAS:
        Tortoise.generate_schemas()
