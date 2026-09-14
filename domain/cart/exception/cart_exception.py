from rest_framework import status
from shared.exceptionalhandler.base_api_exception import BaseAPIException

class CartException(BaseAPIException):
    @classmethod
    def not_found(cls):
        return cls.create(status.HTTP_404_NOT_FOUND, "Cart not found", "CART_NOT_FOUND")

    @classmethod
    def item_not_found(cls):
        return cls.create(status.HTTP_404_NOT_FOUND, "Cart item not found", "CART_ITEM_NOT_FOUND")

    @classmethod
    def duplicate_item(cls):
        return cls.create(status.HTTP_400_BAD_REQUEST, "Product already in cart", "CART_DUPLICATE_ITEM")

    @classmethod
    def product_not_found(cls):
        return cls.create(status.HTTP_404_NOT_FOUND, "Product not found", "PRODUCT_NOT_FOUND")
