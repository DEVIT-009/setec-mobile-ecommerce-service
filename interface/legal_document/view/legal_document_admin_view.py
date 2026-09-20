from rest_framework.views import APIView
from rest_framework.request import Request

from application.legal_document.factory.legal_document_service_factory import legal_document_service_factory
from interface.legal_document.serializer.request.legal_document_request import (
    AdminLegalDocumentCreateRequest,
    AdminLegalDocumentCreateSerializer,
    LEGAL_DOC_TYPE_CHOICES,
)
from shared.responseutils.response_handler import ResponseHandler
from shared.metadata_handler.request_header_utillity import metadata_handler
from shared.permission_handler import require_roles
from shared.pagination.api_paging import ApiPaging


class AdminLegalDocumentListView(APIView):
    """
    GET  /api/v1/admin/legal-documents/  — list all legal documents (all statuses, non-deleted).
    POST /api/v1/admin/legal-documents/  — create a new legal document version.
    """

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def get(self, request: Request, metadata=None):
        doc_type = request.query_params.get('type')
        service = legal_document_service_factory()
        data = service.list_admin(doc_type=doc_type)
        return ResponseHandler.api_success(data)

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def post(self, request: Request, metadata=None):
        serializer = AdminLegalDocumentCreateRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = legal_document_service_factory()
        result = service.create(serializer.validated_data, actor_id=metadata.user_id)
        return ResponseHandler.api_created(result)



class AdminLegalDocumentDetailView(APIView):
    """
    GET    /api/v1/admin/legal-documents/<str:legal_document_id>/
    PUT    /api/v1/admin/legal-documents/<str:legal_document_id>/
    PATCH  /api/v1/admin/legal-documents/<str:legal_document_id>/
    DELETE /api/v1/admin/legal-documents/<str:legal_document_id>/  (soft-delete)
    """

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def get(self, request: Request, legal_document_id=None, metadata=None):
        service = legal_document_service_factory()
        return ResponseHandler.api_success(service.get_admin(str(legal_document_id)))

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def put(self, request: Request, legal_document_id=None, metadata=None):
        service = legal_document_service_factory()
        return ResponseHandler.api_success(service.update(str(legal_document_id), request.data, actor_id=metadata.user_id))

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def patch(self, request: Request, legal_document_id=None, metadata=None):
        service = legal_document_service_factory()
        return ResponseHandler.api_success(service.update(str(legal_document_id), request.data, partial=True, actor_id=metadata.user_id))

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def delete(self, request: Request, legal_document_id=None, metadata=None):
        service = legal_document_service_factory()
        service.soft_delete(str(legal_document_id), actor_id=metadata.user_id)
        return ResponseHandler.api_no_content()
