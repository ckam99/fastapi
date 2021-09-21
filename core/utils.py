import os
from models.auth import User
from asgiref.sync import sync_to_async


@sync_to_async
def email_exists(email: str):
    cn = User.filter(email=email).count()
    return cn > 0


@sync_to_async
def phone_exists(phone: str):
    cn = User.filter(phone=phone).count()
    return cn > 0


def load_models():
    files = ['models.{}'.format(x.name.split('.')[0]) for x in os.scandir(
        'models') if x.is_file() and x.name.endswith('.py')]
    return files


def load_tasks():
    files = ['tasks.{}'.format(x.name.split('.')[0]) for x in os.scandir(
        'models') if x.is_file() and x.name.endswith('.py')]
    return files

# from asgiref.sync import sync_to_async


def unique_code(as_token=True):
    import random
    import uuid
    # import asyncio
    code = uuid.uuid1().hex if as_token else random.randint(209999, 999999)
    # is_exist = asyncio.run(Attempt.filter(code=code).count())
    # if is_exist > 0:
    #     return unique_code(as_token)
    return code
