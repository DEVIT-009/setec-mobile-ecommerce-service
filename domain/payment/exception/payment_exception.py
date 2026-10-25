from rest_framework import status

from shared.exceptionalhandler.base_api_exception import BaseAPIException


class PaymentException(BaseAPIException):
    @classmethod
    def not_found(cls):
        return cls.create(status.HTTP_404_NOT_FOUND, "Payment not found", "PAYMENT_NOT_FOUND")

    @classmethod
    def order_not_found(cls):
        return cls.create(status.HTTP_404_NOT_FOUND, "Order not found", "PAYMENT_ORDER_NOT_FOUND")

    @classmethod
    def order_not_payable(cls, order_status: str):
        return cls.create(
            status.HTTP_409_CONFLICT,
            "Order cannot be paid in its current status",
            "ORDER_NOT_PAYABLE",
            {"order_status": order_status},
        )

    @classmethod
    def idempotency_conflict(cls):
        return cls.create(
            status.HTTP_409_CONFLICT,
            "Idempotency key is already used by another payment",
            "PAYMENT_IDEMPOTENCY_CONFLICT",
        )

    @classmethod
    def batch_idempotency_conflict(cls):
        return cls.create(
            status.HTTP_409_CONFLICT,
            "Idempotency key was already used with a different order set",
            "PAYMENT_BATCH_IDEMPOTENCY_CONFLICT",
        )

    @classmethod
    def orders_not_payable(cls, orders):
        return cls.create(
            status.HTTP_409_CONFLICT,
            "One or more orders cannot be paid",
            "ORDERS_NOT_PAYABLE",
            {"orders": orders},
        )

    @classmethod
    def currency_mismatch(cls):
        return cls.create(
            status.HTTP_409_CONFLICT,
            "All orders in one payment must use the same currency",
            "PAYMENT_CURRENCY_MISMATCH",
        )
