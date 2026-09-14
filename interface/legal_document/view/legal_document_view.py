from rest_framework.views import APIView
from rest_framework.request import Request

from application.legal_document.factory.legal_document_service_factory import legal_document_service_factory
from shared.responseutils.response_handler import ResponseHandler
from shared.metadata_handler.request_header_utillity import metadata_handler


class LegalDocumentListView(APIView):
    @metadata_handler(required_user_id=False)
    def get(self, request: Request, metadata=None):
        doc_type = request.query_params.get('type') 
        service = legal_document_service_factory()
        data = service.list_published(doc_type=doc_type)
        return ResponseHandler.api_success(data)


class LegalDocumentLatestView(APIView):
    @metadata_handler(required_user_id=False)
    def get(self, request: Request, type=None, metadata=None):
        service = legal_document_service_factory()
        data = service.get_latest_by_type(type)
        return ResponseHandler.api_success(data)


class LegalDocumentAcceptView(APIView):
    @metadata_handler(required_user_id=True)
    def post(self, request: Request, legal_document_id=None, metadata=None):
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
        if ip_address and ',' in ip_address:
            ip_address = ip_address.split(',')[0].strip()
        service = legal_document_service_factory()
        data = service.accept(metadata.user_id, str(legal_document_id), ip_address=ip_address)
        return ResponseHandler.api_created(data)


class UserLegalAcceptancesView(APIView):
    @metadata_handler(required_user_id=True)
    def get(self, request: Request, metadata=None):
        service = legal_document_service_factory()
        data = service.list_acceptances(metadata.user_id)
        return ResponseHandler.api_success(data)
