class BadCredentialsError(Exception):
    pass


class TokenExpirateError(Exception):
    pass


class TokenInvalidError(Exception):
    pass


class ModelNotfoundError(Exception):
    pass


class UnAuthorizedError(Exception):
    pass


class FileDoesntExistError(Exception):
    pass


class DbConnectionError(Exception):
    pass
