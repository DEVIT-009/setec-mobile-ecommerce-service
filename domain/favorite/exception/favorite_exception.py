from rest_framework import status
from shared.exceptionalhandler.base_api_exception import BaseAPIException

class FavoriteException(BaseAPIException):
    @classmethod
    def not_found(cls):
        return cls.create(status.HTTP_404_NOT_FOUND, "Favorite not found", "FAVORITE_NOT_FOUND")

    @classmethod
    def already_exists(cls):
        return cls.create(status.HTTP_400_BAD_REQUEST, "Product already in favorites", "FAVORITE_ALREADY_EXISTS")
