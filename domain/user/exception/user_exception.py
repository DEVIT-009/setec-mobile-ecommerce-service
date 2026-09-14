from rest_framework import status
from shared.exceptionalhandler.base_api_exception import BaseAPIException

class UserException(BaseAPIException):
    @classmethod
    def not_found(cls):
        return cls.create(status.HTTP_404_NOT_FOUND, "User not found", "USER_NOT_FOUND")

    @classmethod
    def session_not_found(cls):
        return cls.create(status.HTTP_404_NOT_FOUND, "Session not found", "SESSION_NOT_FOUND")
