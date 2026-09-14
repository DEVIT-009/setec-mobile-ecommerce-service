from rest_framework import status
from shared.exceptionalhandler.base_api_exception import BaseAPIException

class OrderException(BaseAPIException):
    @classmethod
    def not_found(cls):
        return cls.create(status.HTTP_404_NOT_FOUND, "Order not found", "ORDER_NOT_FOUND")

    @classmethod
    def cannot_cancel(cls):
        return cls.create(status.HTTP_400_BAD_REQUEST, "Order cannot be cancelled at this stage", "ORDER_CANNOT_CANCEL")

    @classmethod
    def duplicate_order(cls):
        return cls.create(status.HTTP_409_CONFLICT, "Duplicate order request", "ORDER_DUPLICATE")

    @classmethod
    def empty_cart(cls):
        return cls.create(status.HTTP_400_BAD_REQUEST, "No selected items in cart", "CART_EMPTY")
