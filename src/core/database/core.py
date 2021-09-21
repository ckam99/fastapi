from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise
from fastapi import FastAPI
from core import settings
import logging


async def connect_db(app: FastAPI):

    register_tortoise(
        app,
        config=settings.TORTOISE_ORM,
        generate_schemas=settings.DATABASE_GENERATE_SCHEMAS,
        add_exception_handlers=True
    )
    if settings.DATABASE_GENERATE_SCHEMAS:
        await Tortoise.generate_schemas()
    logging.info('Tortoise-ORM started, %s, %s',
                 Tortoise._connections, Tortoise.apps)
