from flask_restx import Api
from ..utils import SuccessResponse, ErrorResponse, HttpError
from ..constants import HttpCode

# routes
from .convert import convert

routes = Api(
    title="OCR API",
    version="1.0",
    description="An API for OCR"
)

# register routes
routes.add_namespace(convert, path="/api/image")

@routes.errorhandler(HttpError)
def handle_error(error):
    """
    This function handles all custom thrown error including
    Unauthorized, Forbidden, and Validation errors
    """

    return ErrorResponse(
        message=error.message,
        errors=error.errors
    ).to_dict(), error.http_code
