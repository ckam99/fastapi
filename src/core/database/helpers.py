from apps.base.models import ConfirmAction
import random
import uuid
# from asgiref.sync import sync_to_async
import asyncio


def unique_code(as_token=True):
    code = uuid.uuid1().hex if as_token else random.randint(209999, 999999)
    # is_exist = asyncio.run(ConfirmAction.filter(code=code).count())
    # if is_exist > 0:
    #     return unique_code(as_token)
    return code
