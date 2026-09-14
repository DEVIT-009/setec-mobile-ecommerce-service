from rest_framework import status
from shared.exceptionalhandler.base_api_exception import BaseAPIException


class ProductException(BaseAPIException):

    @classmethod
    def not_found(cls, message: str = "Product not found"):
        return cls.create(status.HTTP_404_NOT_FOUND, message, "PRODUCT_NOT_FOUND")

    @classmethod
    def already_exists(cls, message: str = "Product with this slug already exists in this store"):
        return cls.create(status.HTTP_400_BAD_REQUEST, message, "PRODUCT_ALREADY_EXISTS")

    already_exist = already_exists
