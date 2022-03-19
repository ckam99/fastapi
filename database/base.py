from tortoise.contrib.fastapi import register_tortoise
from tortoise import BaseDBAsyncClient, Tortoise
from fastapi import FastAPI
from core.settings import TORTOISE_ORM
import logging

logger = logging.getLogger(__name__)


def connect_db(app: FastAPI):

    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=False,
        add_exception_handlers=True
    )
    logger.info('Tortoise-ORM started, %s, %s',
                Tortoise._connections, Tortoise.apps)


async def get_database(connection: str = 'default') -> BaseDBAsyncClient:
    await Tortoise.init(TORTOISE_ORM)
    return Tortoise.get_connection(connection_name=connection)


async def get_test_database() -> BaseDBAsyncClient:
    await Tortoise.init(db_url='sqlite://db.sqlite3',
                        modules={"models": TORTOISE_ORM["apps"]['models']['models']})
    await Tortoise.generate_schemas()
    return Tortoise.get_connection(connection_name='default')
