from rest_framework import status
from shared.exceptionalhandler.base_api_exception import BaseAPIException

class LegalException(BaseAPIException):
    @classmethod
    def not_found(cls):
        return cls.create(status.HTTP_404_NOT_FOUND, "Legal document not found", "LEGAL_DOC_NOT_FOUND")

    @classmethod
    def already_accepted(cls):
        return cls.create(status.HTTP_400_BAD_REQUEST, "Document already accepted", "LEGAL_ALREADY_ACCEPTED")
