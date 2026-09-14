from rest_framework import status
from shared.exceptionalhandler.base_api_exception import BaseAPIException


class StoreException(BaseAPIException):

    @classmethod
    def not_found(cls, message: str = "Store not found"):
        return cls.create(status.HTTP_404_NOT_FOUND, message, "STORE_NOT_FOUND")

    @classmethod
    def already_exists(cls, message: str = "Store with this slug already exists"):
        return cls.create(status.HTTP_400_BAD_REQUEST, message, "STORE_ALREADY_EXISTS")

    @classmethod
    def invalid_owner(cls, message: str = "Invalid store owner"):
        return cls.create(status.HTTP_400_BAD_REQUEST, message, "INVALID_STORE_OWNER")

    already_exist = already_exists
