from fastapi import HTTPException

from starlette import status
from models.auth import User, Role, Attempt
from schemas.auth import (LoginSchema, RegisterSchema, RoleInSchema)
from core.security import OAuth
from datetime import datetime
from typing import List


class AuthAPIView():

    async def register(self, payload: RegisterSchema) -> User:

        user_obj = User(**payload.dict())
        user_obj.set_password(payload.password)
        await user_obj.save()
        return user_obj

    async def login(self, payload: LoginSchema):
        user = await OAuth.authenticate(payload.email, payload.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Email or password incorrect.')
        return OAuth.generate_token(dict(user))

    async def oauth_login(self, username: str, password: str):
        user = await OAuth.authenticate(username, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Email or password incorrect.')
        return OAuth.generate_token(dict(user))

    async def confirm_email(self, email: str, code: str) -> User:
        confirmer = await Attempt.filter(email=email, code=code).first()
        if confirmer:
            diff_date = datetime.now() - confirmer.created_at.replace(tzinfo=None)
            if diff_date.total_seconds() > 86400:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail='Your confirmation token is expirated.')
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


class RoleAPIView():

    async def list(self) -> List[Role]:
        return await Role.all()

    async def create(self, credentials: RoleInSchema) -> Role:
        credentials.name = credentials.name.upper()
        return await Role.create(**credentials.dict())
