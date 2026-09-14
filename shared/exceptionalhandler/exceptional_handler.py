import logging

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError, AuthenticationFailed

from shared.exceptionalhandler.error_constant_exception import ErrorConstantException
from shared.exceptionalhandler.exception_helper import create_error_response, flatten_validation_errors
from shared.exceptionalhandler.http_error_response import HttpBodyResponse
from shared.exceptionalhandler.http_exception import HttpException

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    request = context.get("request")

    # 🔹 Serializer validation error (400 with body)
    if isinstance(exc, ValidationError):
        error_response = create_error_response(
            exc,
            ErrorConstantException.VALIDATION_ERROR,
            body_request_error=flatten_validation_errors(exc.detail),
        )

        body = HttpBodyResponse(
            status=status.HTTP_400_BAD_REQUEST,
            message=ErrorConstantException.VALIDATION_ERROR.message,
            error=error_response,
        )
        return Response(body.to_dict(), status=status.HTTP_400_BAD_REQUEST)

    # 🔹 Authentication error
    if isinstance(exc, AuthenticationFailed):
        return Response(
            {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Invalid username or password",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # 🔹 Domain HttpException
    if isinstance(exc, HttpException):
        error_response = create_error_response(exc, exc.error)
        body = HttpBodyResponse(
            status=exc.status_code,
            message=str(exc),
            error=error_response,
        )
        return Response(body.to_dict(), status=exc.status_code)

    # 🔹 Let DRF handle the rest
    response = exception_handler(exc, context)
    if response is not None:
        return response

    # 🔹 Fallback 500
    logger.error("Unhandled Exception", exc_info=True)

    error_response = create_error_response(exc, ErrorConstantException.UNKNOWN_ERROR)
    body = HttpBodyResponse(
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=str(exc) or ErrorConstantException.ERROR.message,
        error=error_response,
    )
    return Response(body.to_dict(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

