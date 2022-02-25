from fastapi import status
from fastapi.responses import JSONResponse
from models.users import User
from schemas.base import ValidationSchema


class UserValidator():
    async def validate_unique_fields(*args, **kwargs):
        errors = []
        if 'email' in kwargs:
            obj = await User.filter(email=kwargs['email']).exists()
            if obj:
                errors.append(ValidationSchema(
                    field='email', type='type_error.unique', msg='Email already exist'))
        if 'username' in kwargs:
            obj = await User.filter(username=kwargs['username']).exists()
            if obj:
                errors.append(ValidationSchema(
                    field='username', type='type_error.unique', msg='Username already exist'))
        if 'phone' in kwargs:
            obj = await User.filter(phone=kwargs['phone']).exists()
            if obj:
                errors.append(ValidationSchema(
                    field='phone', type='type_error.unique', msg='Phone already exist'))
        return JSONResponse(content={'errors': errors}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
