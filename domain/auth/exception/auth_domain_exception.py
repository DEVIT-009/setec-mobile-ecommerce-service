from rest_framework import status
from shared.exceptionalhandler.base_api_exception import BaseAPIException

class AuthDomainException(BaseAPIException):
    @classmethod
    def invalid_credentials(cls):
        return cls.create(status.HTTP_401_UNAUTHORIZED, "Invalid email or password", "INVALID_CREDENTIALS")

    @classmethod
    def email_already_exists(cls):
        return cls.create(status.HTTP_400_BAD_REQUEST, "Email already registered", "EMAIL_ALREADY_EXISTS")

    @classmethod
    def account_blocked(cls):
        return cls.create(status.HTTP_403_FORBIDDEN, "Account is blocked", "ACCOUNT_BLOCKED")

    @classmethod
    def account_inactive(cls):
        return cls.create(status.HTTP_403_FORBIDDEN, "Account is inactive", "ACCOUNT_INACTIVE")

    @classmethod
    def invalid_token(cls):
        return cls.create(status.HTTP_401_UNAUTHORIZED, "Invalid or expired token", "INVALID_TOKEN")
