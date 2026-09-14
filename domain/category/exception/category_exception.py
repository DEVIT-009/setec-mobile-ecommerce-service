from rest_framework import status
from shared.exceptionalhandler.base_api_exception import BaseAPIException


class CategoryException(BaseAPIException):

    @classmethod
    def not_found(cls, message: str = "Category not found"):
        return cls.create(status.HTTP_404_NOT_FOUND, message, "CATEGORY_NOT_FOUND")

    @classmethod
    def already_exists(cls, message: str = "Category with this slug or name already exists"):
        return cls.create(status.HTTP_400_BAD_REQUEST, message, "CATEGORY_ALREADY_EXISTS")

    @classmethod
    def invalid_parent(cls, message: str = "Invalid parent category"):
        return cls.create(status.HTTP_400_BAD_REQUEST, message, "INVALID_PARENT_CATEGORY")