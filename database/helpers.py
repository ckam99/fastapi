from fastapi import Depends
from models.users import User, VerifyCode
from core.security import JWTBearer, verify_password, decode_token, oauth2_scheme
from jose import ExpiredSignatureError, JWTError
from core.exceptions import (
    TokenExpirateError, TokenInvalidError, UnAuthorizedError,
    BadCredentialsError
)


async def is_authenticated(username: str, password: str) -> bool | User:
    user = await User.get_or_none(email=username)
    if not user:
        return False
    if not verify_password(password):
        return False
    return user


async def authenticate(username: str, password: str) -> User:
    user = await User.get_or_none(email=username)
    if not user:
        raise BadCredentialsError('Email or password incorrect.')
    if not verify_password(password, user.password):
        raise BadCredentialsError('Email or password incorrect.')
    return user


async def get_current_user(token: str = Depends(JWTBearer())):
    try:
        decoded_token = decode_token(token)
        user = await User.get_or_none(id=decoded_token.get('id'))
        if not user:
            raise UnAuthorizedError("Invalid authentication credentials")
        return user
    except ExpiredSignatureError:
        raise TokenExpirateError("Token expired. Get new one")
    except JWTError:
        raise TokenInvalidError("Invalid Token")


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.is_actif:
        raise UnAuthorizedError("Inactive user")
    return current_user


async def unique_code(as_token=True):
    import random
    import uuid
    code = uuid.uuid1().hex if as_token else random.randint(209999, 999999)
    is_exist = await VerifyCode.filter(code=code).count()
    if is_exist > 0:
        return await unique_code(as_token)
    return code


async def generate_verify_code(email: str, as_token=True):
    code = await unique_code(as_token)
    await VerifyCode.create(email=email, code=code)
    return code
