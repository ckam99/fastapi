import os
from core.schemas import ValidationSchema
# from asgiref.sync import sync_to_async


def load_models():
    files = ['models.{}'.format(x.name.split('.')[0]) for x in os.scandir(
        'models') if x.is_file() and x.name.endswith('.py')]
    return files


def load_tasks():
    files = ['tasks.{}'.format(x.name.split('.')[0]) for x in os.scandir(
        'models') if x.is_file() and x.name.endswith('.py')]
    return files


def unique_code(as_token=True):
    import random
    import uuid
    # import asyncio
    code = uuid.uuid1().hex if as_token else random.randint(209999, 999999)
    # is_exist = asyncio.run(Attempt.filter(code=code).count())
    # if is_exist > 0:
    #     return unique_code(as_token)
    return code


def format_validation_errors(errors):
    err = [ValidationSchema(
        field=e['loc'][-1], type=e['type'], msg=e['msg']).dict() for e in errors]
    return err
