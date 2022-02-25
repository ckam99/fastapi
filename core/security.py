from fastapi import Request
from fastapi.security import (
    OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials)
from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from core.exceptions import TokenExpirateError
from core.settings import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, JWT_TOKEN_ALGORITHM, AUTH_URL

oauth2_scheme = OAuth2PasswordBearer(AUTH_URL)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password):
    return pwd_context.hash(password)


def decode_token(token: str):
    return jwt.decode(
        token, SECRET_KEY, algorithms=[JWT_TOKEN_ALGORITHM])


def encode_token(data: dict) -> str:
    return jwt.encode(data, SECRET_KEY, algorithm=JWT_TOKEN_ALGORITHM)


def create_access_token(user_obj: dict):
    if 'password' in user_obj:
        del user_obj['password']
    expire_at = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = encode_token(user_obj)
    user_obj['access_token'] = token
    user_obj['token_type'] = 'bearer'
    user_obj['token_expire_at'] = str(expire_at)
    return user_obj


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            token = decode_token(credentials.credentials)
            if token is None:
                raise TokenExpirateError("Invalid auth token")
            return credentials.credentials
        else:
            raise TokenExpirateError("Invalid auth token")
