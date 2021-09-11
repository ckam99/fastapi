from fastapi.exceptions import HTTPException
from tortoise.query_utils import Q
from starlette import status
from .models import User, Role
from .schemas import (LoginSchema, RegisterSchema, RoleCredentialSchema)
from core.contrib.security import OAuth


class AuthAPIView():

    @staticmethod
    async def register(self, payload: RegisterSchema):
        obj = await User.filter(Q(email=payload.email) | Q(username=payload.username)).first()
        if obj:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Email or username already exist')
        user_obj = User(**payload.dict())
        user_obj.set_password(payload.password)
        await user_obj.save()
        return user_obj

    @staticmethod
    async def login(self, payload: LoginSchema):
        user = await OAuth.authenticate(payload.email, payload.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Email or password incorrect.')
        return OAuth.generate_token(dict(user))

    @staticmethod
    async def oauth_login(self, username: str, password: str):
        user = await OAuth.authenticate(username, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Email or password incorrect.')
        return OAuth.generate_token(dict(user))


class UserAPIView():

    @staticmethod
    async def list(self):
        return await User.all()

    @staticmethod
    def update(self, payload):
        pass


class RoleAPIView():

    @staticmethod
    async def list(self):
        return await Role.all()

    @staticmethod
    async def create(self, credentials: RoleCredentialSchema):
        credentials.name = credentials.name.upper()
        return await Role.create(**credentials.dict())
