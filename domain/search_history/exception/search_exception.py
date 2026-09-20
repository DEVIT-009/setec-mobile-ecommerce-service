from rest_framework import status
from shared.exceptionalhandler.base_api_exception import BaseAPIException


class SearchHistoryException(BaseAPIException):
    @classmethod
    def not_found(cls, message: str = "Search history record not found"):
        return cls.create(status.HTTP_404_NOT_FOUND, message, "SEARCH_HISTORY_NOT_FOUND")
