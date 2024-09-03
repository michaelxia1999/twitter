from app.errors import Error
from app.exc.core import ApplicationError
from app.exc.utils import format_validation_error_location
from app.utils import create_response
from fastapi import Request
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


async def request_validation_error_handler(request: Request, e: RequestValidationError):
    # override fastapi default validation schema
    error = e.errors()[0]

    if error["msg"] == "JSON decode error":
        location = "body"
        detail = "Invalid format"
    else:
        location = format_validation_error_location(error_location=error["loc"])
        detail = error["msg"]

    body = Error(location=location, value=error["input"], detail=detail)
    return create_response(status_code=400, body=body)


async def response_validation_error_handler(request: Request, e: ResponseValidationError):
    # Responses are returned using create_response(which uses JSONResponse under the hood)
    # Do not use response_model inside router because you can only provide 1 response model, it doesn't work if your api can return different models
    # Return using JSONResponse directly and manually add response schemas to openapi for documentation
    print("All routes should return using create_response from app.core")
    return create_response(status_code=500)


async def validation_error_handler(request: Request, e: ValidationError):
    # Handles all pydantic validation errors within the application
    error = e.errors()[0]
    location = format_validation_error_location(error_location=error["loc"])
    content = Error(location=location, value=error["input"], detail=error["msg"])
    print("Pydantic error: ", content)
    return create_response(status_code=500)


async def application_error_handler(request: Request, e: ApplicationError):
    return create_response(status_code=e.status_code, body=e.body, headers=e.headers)


async def http_error_handler(request: Request, e: StarletteHTTPException):
    return create_response(status_code=e.status_code)
