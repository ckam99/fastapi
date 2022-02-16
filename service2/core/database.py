from fastapi import FastAPI
from tortoise import BaseDBAsyncClient, Tortoise
from tortoise.contrib.fastapi import register_tortoise
from settings import TORTOISE_ORM_CONFIG

# db_config = {
#     "connections": {
#         "default": {
#             "engine": "tortoise.backends.sqlite",
#             "credentials": {"file_path": "db.sqlite3"},
#         },
#     },
#     "apps": {
#         "models": {
#             "models": ["models"],
#             "default_connection": "default"
#         }
#     },
# }


async def get_database(connection: str = 'default') -> BaseDBAsyncClient:
    # await Tortoise.init(db_url='sqlite://db.sqlite3', modules={"models": ["models"]})
    await Tortoise.init(TORTOISE_ORM_CONFIG)
    return Tortoise.get_connection(connection_name=connection)


def connect_db(app: FastAPI):
    register_tortoise(
        app,
        config=TORTOISE_ORM_CONFIG,
        # db_url='sqlite://db.sqlite3',
        # modules={"models": ["models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    print('database connected')
