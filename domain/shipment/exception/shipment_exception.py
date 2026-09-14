from rest_framework import status
from shared.exceptionalhandler.base_api_exception import BaseAPIException

class ShipmentException(BaseAPIException):
    @classmethod
    def not_found(cls):
        return cls.create(status.HTTP_404_NOT_FOUND, "Shipment not found", "SHIPMENT_NOT_FOUND")
