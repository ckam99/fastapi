
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise, BaseDBAsyncClient
from .settings import TORTOISE_ORM_CONFIG


async def get_database(connection: str = 'default') -> BaseDBAsyncClient:
    await Tortoise.init(TORTOISE_ORM_CONFIG)
    return Tortoise.get_connection(connection_name=connection)


def init_database(app):
    register_tortoise(app,
                      config=TORTOISE_ORM_CONFIG,
                      add_exception_handlers=True,
                      generate_schemas=True
                      )
    print('database connected')
