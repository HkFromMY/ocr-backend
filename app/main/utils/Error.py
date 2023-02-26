from typing import Type
from ..constants import HttpCode, RecordStatus

class HttpError(Exception):
    http_code: int
    message: str
    errors: dict

    def __init__(self, http_code: int, message: str, errors={}):
        self.http_code = http_code
        self.message = message
        self.errors = errors

class NotFoundError(HttpError):
    def __init__(self, message: str, errors={}):
        super().__init__(HttpCode.NOT_FOUND, message, errors)

class ValidationError(HttpError):
    def __init__(self, message: str, errors={}):
        super().__init__(HttpCode.UNPROCESSABLE_ENTITY, message, errors)

class UnauthorizedError(HttpError):
    def __init__(self, message: str, errors={}):
        super().__init__(HttpCode.UNAUTHORIZED, message, errors)

class ForbiddenError(HttpError):
    def __init__(self, message: str, errors={}):
        super().__init__(HttpCode.FORBIDDEN, message, errors)

class BadRequestError(HttpError):
    def __init__(self, message: str, errors={}):
        super().__init__(HttpCode.BAD_REQUEST, message, errors)
