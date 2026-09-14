import traceback

from shared.exceptionalhandler.http_error_response import HttpBodyErrorResponse


def create_error_response(exc, error_constant, body_request_error=None):
    return HttpBodyErrorResponse(
        type=exc.__class__.__name__,
        code=error_constant.code,
        message=error_constant.message,
        error=f"{exc.__class__.__name__}: {str(exc)}",
        bodyRequestError=body_request_error,
    )

def flatten_validation_errors(detail):
    errors = {}
    for field, messages in detail.items():
        errors[field] = messages[0] if isinstance(messages, list) else str(messages)
    return errors
