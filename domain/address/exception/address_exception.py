from rest_framework import status
from shared.exceptionalhandler.base_api_exception import BaseAPIException


class AddressException(BaseAPIException):

    @classmethod
    def not_found(cls, message: str = "Address not found"):
        return cls.create(status.HTTP_404_NOT_FOUND, message, "ADDRESS_NOT_FOUND")

    @classmethod
    def invalid_country_code(cls, message: str = "country_code must be 2 characters"):
        return cls.create(status.HTTP_400_BAD_REQUEST, message, "INVALID_COUNTRY_CODE")

    @classmethod
    def invalid_input(cls, message: str = "Invalid address data"):
        return cls.create(status.HTTP_400_BAD_REQUEST, message, "INVALID_ADDRESS_DATA")
