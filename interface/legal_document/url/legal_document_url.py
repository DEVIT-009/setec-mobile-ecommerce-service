from django.urls import path
from interface.legal_document.view.legal_document_view import (
    LegalDocumentListView,
    LegalDocumentLatestView,
)

# Public legal document routes (no authentication required)
urlpatterns = [
    path('legal-documents/', LegalDocumentListView.as_view(), name='legal-document-list'),
    path('legal-documents/<str:type>/latest/', LegalDocumentLatestView.as_view(), name='legal-document-latest'),
]
