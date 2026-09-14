from rest_framework import status
from shared.exceptionalhandler.base_api_exception import BaseAPIException


class TagException(BaseAPIException):

    @classmethod
    def not_found(cls, message: str = "Tag not found"):
        return cls.create(status.HTTP_404_NOT_FOUND, message, "TAG_NOT_FOUND")

    @classmethod
    def already_exists(cls, message: str = "Tag with this slug or name already exists"):
        return cls.create(status.HTTP_400_BAD_REQUEST, message, "TAG_ALREADY_EXISTS")
