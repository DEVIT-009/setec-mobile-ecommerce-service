from rest_framework import status
from shared.exceptionalhandler.base_api_exception import BaseAPIException

class SupportException(BaseAPIException):
    @classmethod
    def not_found(cls):
        return cls.create(status.HTTP_404_NOT_FOUND, "Support ticket not found", "TICKET_NOT_FOUND")
