from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise
from fastapi import FastAPI


def connect_db(app:FastAPI, generate_schemas=True):
    register_tortoise(
     app,
     db_url="sqlite://sqlite.db",
     modules={"models": ["models"]},
     generate_schemas=True,
     add_exception_handlers=True,
    )
    if generate_schemas:
        Tortoise.generate_schemas()

    
