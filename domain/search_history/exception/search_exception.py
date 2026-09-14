from rest_framework import status
from shared.exceptionalhandler.base_api_exception import BaseAPIException

class SearchException(BaseAPIException):
    @classmethod
    def not_found(cls):
        return cls.create(status.HTTP_404_NOT_FOUND, "Search record not found", "SEARCH_NOT_FOUND")
