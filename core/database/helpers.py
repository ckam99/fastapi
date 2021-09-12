from base.models import ConfirmAction, User
import random
import uuid
from dotenv import load_dotenv
load_dotenv('.env')


async def unique_code(as_token=True):
    code = uuid.uuid1().hex if as_token else random.randint(209999, 999999)
    is_exist = await ConfirmAction.filter(code=code).count()
    if is_exist > 0:
        return await unique_code(as_token)
    return code


async def get_users():
    users = await User.all()
    return users
