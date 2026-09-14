from rest_framework import status

from shared.exceptionalhandler.base_api_exception import BaseAPIException


class AuthException(BaseAPIException):

    @classmethod
    def unauthorized(cls):
        return cls.create(
            status.HTTP_401_UNAUTHORIZED,
            "Unauthorized",
            error_code="AUTH_401"
        )

    @classmethod
    def forbidden(cls):
        return cls.create(
            status.HTTP_403_FORBIDDEN,
            "Forbidden",
            error_code="AUTH_403"
        )
