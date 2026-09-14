from rest_framework.exceptions import APIException


class BaseAPIException(APIException):
    def __init__(self, status_code, message, error_code="UNKNOWN_ERROR", error_details=None):
        self.status_code = status_code
        self.message = message
        self.error_code = error_code
        self.error_details = error_details or {}
        self.detail = {
            "status": status_code,
            "message": message,
            "data": None,
            "error": {
                "type": self.__class__.__name__,
                "code": error_code,
                "message": message,
                "error": f"{self.__class__.__name__}.{message}",
                **self.error_details
            }
        }

    @classmethod
    def create(cls, status_code, message, error_code="UNKNOWN_ERROR", error_details=None):
        return cls(status_code, message, error_code, error_details)
