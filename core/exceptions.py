from fastapi import Request, HTTPException, Response
from fastapi.routing import APIRoute
from fastapi.exceptions import RequestValidationError
from typing import Callable


class UniqueEmailError(Exception):
    def __init__(self, value: str, message: str):
        self.value = value
        self.message = message
        return super().__init__(message)


class UniqueUsernameError(Exception):
    def __init__(self, value: str, message: str):
        self.value = value
        self.message = message
        return super().__init__(message)


class UniquePhoneError(Exception):
    def __init__(self, value: str, message: str):
        self.value = value
        self.message = message
        return super().__init__(message)


class RegisterExceptionRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except RequestValidationError as exc:
                body = await request.body()
                detail = {"errors": exc.errors(), "body": body.decode()}
                raise HTTPException(status_code=422, detail=detail)
            except UniqueEmailError as exc:
                raise HTTPException(status_code=422, detail=exc.message)

        return custom_route_handler
