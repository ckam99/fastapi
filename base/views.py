from core.contrib.views import BaseModelView
from .models import User
from .schemas import RegisterSchema


class AuthView():
    model = User

    async def register(user: RegisterSchema):
        user_obj = User(**user.dict())
        user_obj.set_password(user.password)
        await user_obj.save()
        return user_obj
