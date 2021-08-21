
from tortoise.query_utils import Q
from .models import User


async def unique_email(user: User):
    obj = await User.filter(Q(email=user.email) | Q(username=user.username)).first()
    return obj
    if obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Email already exist')


def validate_email(email):
    import re
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(not re.fullmatch(regex, email)):
        raise ValueError("Valid Email")
