from rest_framework import status

from shared.exceptionalhandler.base_api_exception import BaseAPIException

class MetadataException(BaseAPIException):
    @staticmethod
    def unauthorized():
        return MetadataException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Unauthorized"
        )

    @staticmethod
    def required_merchant_id():
        return MetadataException(
            status_code=status.HTTP_404_NOT_FOUND,
            message="The X-Merchant-ID is required"
        )

    @staticmethod
    def require_app_id():
        return MetadataException(
            status_code=status.HTTP_404_NOT_FOUND,
            message="The X-App-ID is required"
        )
