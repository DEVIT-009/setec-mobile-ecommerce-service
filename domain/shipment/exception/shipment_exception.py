from rest_framework import status
from shared.exceptionalhandler.base_api_exception import BaseAPIException

class ShipmentException(BaseAPIException):
    @classmethod
    def not_found(cls):
        return cls.create(status.HTTP_404_NOT_FOUND, "Shipment not found", "SHIPMENT_NOT_FOUND")

    @classmethod
    def invalid_status_transition(cls, from_status: str, to_status: str):
        return cls.create(
            status.HTTP_409_CONFLICT,
            f"Shipment cannot transition from {from_status} to {to_status}",
            "SHIPMENT_INVALID_STATUS_TRANSITION",
            {"from_status": from_status, "to_status": to_status},
        )

    @classmethod
    def order_not_ready(cls, order_status: str, required_status: str):
        return cls.create(
            status.HTTP_409_CONFLICT,
            "Order is not ready for this shipment action",
            "ORDER_NOT_READY_FOR_SHIPMENT",
            {"order_status": order_status, "required_status": required_status},
        )
