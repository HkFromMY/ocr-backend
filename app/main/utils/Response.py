from typing import Type

class Response:
    """
    General response object to be sent to client
    Consists of 3 attributes
    """

    status: str
    message: str
    data: dict

    def __init__(self, status: str, message: str, data={}):
        self.status = status
        self.message = message
        self.data = data

    def to_dict(self) -> dict:
        # convert to dictionary data type to be sent t oclient
        return {
            "status": self.status,
            "message": self.message,
            "data": self.data
        }

class SuccessResponse(Response):
    """
    Format successful response
    """

    def __init__(self, message: str, data={}):
        super().__init__("success", message, data)

class ErrorResponse(Response):
    """
    Format response when http error are thrown
    """

    errors: dict

    def __init__(self, message: str, errors={}):
        self.status = "failed"
        self.message = message
        self.errors = errors

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "message": self.message,
            "errors": self.errors
        }

