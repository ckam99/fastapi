from apps.base.models import ConfirmAction, User
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


async def email_exists(email: str):
    cn = await User.filter(email=email).count()
    return cn > 0


async def phone_exists(phone: str):
    cn = await User.filter(phone=phone).count()
    return cn > 0
