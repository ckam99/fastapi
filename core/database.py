from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise
from fastapi import FastAPI
import settings


def connect_db(app: FastAPI):
    register_tortoise(
        app,
        config=settings.TORTOISE_ORM,
        generate_schemas=False,
        add_exception_handlers=True,
    )


async def init_db():
    await Tortoise.init(
        config=settings.TORTOISE_ORM,
    )
    if settings.DATABASE_GENERATE_SCHEMAS:
        await Tortoise.generate_schemas()
