from fastapi.exceptions import HTTPException
from tortoise.query_utils import Q
from starlette import status
from .models import User, Role, ConfirmAction
from .schemas import (LoginSchema, RegisterSchema, RoleCredentialSchema)
from core.contrib.security import OAuth
from datetime import datetime
from typing import List


class AuthService():

    @staticmethod
    async def register(payload: RegisterSchema) -> User:
        obj = await User.filter(Q(email=payload.email) | Q(username=payload.username)).first()
        if obj:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Email or username already exist')
        user_obj = User(**payload.dict())
        user_obj.set_password(payload.password)
        await user_obj.save()
        return user_obj

    @staticmethod
    async def login(payload: LoginSchema):
        user = await OAuth.authenticate(payload.email, payload.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Email or password incorrect.')
        return OAuth.generate_token(dict(user))

    @staticmethod
    async def oauth_login(username: str, password: str):
        user = await OAuth.authenticate(username, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Email or password incorrect.')
        return OAuth.generate_token(dict(user))

    @staticmethod
    async def confirm_email(email: str, code: str) -> User:
        confirmer = await ConfirmAction.filter(email=email, code=code).first()
        if confirmer:
            diff_date = datetime.now() - confirmer.created_at.replace(tzinfo=None)
            if diff_date.total_seconds() > 86400:
                raise serializers.ValidationError(
                    'Your confirmation token is expirated.'
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='corrupted credentials.')
        user = await User.filter(email=email).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='No user found with email.')
        user.email_confirmed_at = datetime.now()
        user.save()
        return user


class UserService():

    @staticmethod
    async def list() -> List[User]:
        return await User.all()

    @staticmethod
    def update(payload):
        pass


class RoleService():

    @staticmethod
    async def list() -> List[Role]:
        return await Role.all()

    @staticmethod
    async def create(credentials: RoleCredentialSchema) -> Role:
        credentials.name = credentials.name.upper()
        return await Role.create(**credentials.dict())
