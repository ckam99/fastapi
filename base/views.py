from fastapi.exceptions import HTTPException
from tortoise.query_utils import Q
from starlette import status
from .models import User
from .schemas import LoginSchema, RegisterSchema
from core.contrib.security import OAuth

oauth = OAuth()


class AuthAPIView():

    async def register(self, payload: RegisterSchema):
        obj = await User.filter(Q(email=payload.email) | Q(username=payload.username)).first()
        if obj:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Email or username already exist')
        user_obj = User(**payload.dict())
        user_obj.set_password(payload.password)
        await user_obj.save()
        return user_obj

    async def login(self, payload: LoginSchema):
        user = await oauth.authenticate(payload.email, payload.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Email or password incorrect.')
        return oauth.generate_token(dict(user))

    async def oauth_login(self, username: str, password: str):
        user = await oauth.authenticate(username, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Email or password incorrect.')
        return oauth.generate_token(dict(user))


class UserAPIView():

    async def list(self):
        return await User.all()

    def update(self, payload):
        pass
