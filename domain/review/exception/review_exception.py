from rest_framework import status
from shared.exceptionalhandler.base_api_exception import BaseAPIException

class ReviewException(BaseAPIException):
    @classmethod
    def not_found(cls):
        return cls.create(status.HTTP_404_NOT_FOUND, "Review not found", "REVIEW_NOT_FOUND")

    @classmethod
    def duplicate_review(cls):
        return cls.create(status.HTTP_400_BAD_REQUEST, "Already reviewed this item", "REVIEW_DUPLICATE")

    @classmethod
    def invalid_rating(cls):
        return cls.create(status.HTTP_400_BAD_REQUEST, "Rating must be between 1 and 5", "INVALID_RATING")

    @classmethod
    def product_not_found(cls):
        return cls.create(status.HTTP_404_NOT_FOUND, "Product not found", "PRODUCT_NOT_FOUND")

    @classmethod
    def order_item_not_found(cls):
        return cls.create(status.HTTP_404_NOT_FOUND, "Order item not found", "ORDER_ITEM_NOT_FOUND")

    @classmethod
    def invalid_order_item(cls, message: str = "Order item does not belong to this user or product"):
        return cls.create(status.HTTP_400_BAD_REQUEST, message, "INVALID_ORDER_ITEM")
