

class AppBaseException(Exception):
    def __init__(self, value: str, message: str):
        self.value = value
        self.message = message
        return super().__init__(message)


class ModelNotFoundException(AppBaseException):
    pass
