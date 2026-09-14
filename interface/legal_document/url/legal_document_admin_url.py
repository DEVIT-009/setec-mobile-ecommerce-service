from django.urls import path
from interface.legal_document.view.legal_document_admin_view import (
    AdminLegalDocumentListView,
    AdminLegalDocumentDetailView,
)

# Admin legal document management endpoints — require authentication + admin role.
# GET    /api/v1/admin/legal-documents/
# POST   /api/v1/admin/legal-documents/
# GET    /api/v1/admin/legal-documents/<uuid:legal_document_id>/
# PUT    /api/v1/admin/legal-documents/<uuid:legal_document_id>/
# PATCH  /api/v1/admin/legal-documents/<uuid:legal_document_id>/
# DELETE /api/v1/admin/legal-documents/<uuid:legal_document_id>/
urlpatterns = [
    path('legal-documents/', AdminLegalDocumentListView.as_view(), name='admin-legal-document-list'),
    path('legal-documents/<uuid:legal_document_id>/', AdminLegalDocumentDetailView.as_view(), name='admin-legal-document-detail'),
]
