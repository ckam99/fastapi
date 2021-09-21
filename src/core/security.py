from fastapi import status, Depends, HTTPException
from fastapi.security import (OAuth2PasswordBearer, OAuth2PasswordRequestForm)
from typing import Optional
import jwt
from datetime import datetime, timedelta
from apps.base.models import User

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


class OAuth():

    @staticmethod
    async def authenticate(username: str, password: str):
        user = await User.get_or_none(email=username)
        if not user:
            return False
        if not user.verify_password(password):
            return False
        return user

    @staticmethod
    def generate_token(user_obj: dict):
        if 'password' in user_obj:
            del user_obj['password']
        expire_at = datetime.utcnow(
        ) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        token = jwt.encode({
            'id': user_obj['id'],
            'exp':  expire_at,
            'email': user_obj['email'],
        }, SECRET_KEY)
        user_obj['access_token'] = token
        user_obj['token_type'] = 'bearer'
        user_obj['token_expire_at'] = expire_at
        return user_obj

    @staticmethod
    async def get_current_user(token: str = Depends(oauth2_scheme)):
        try:
            decode_token = jwt.decode(
                token, SECRET_KEY, algorithms=[ALGORITHM])
            user = await User.get_or_none(id=decode_token.get('id'))
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return user
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired. Get new one")
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
