from django.urls import path
from interface.legal_document.view.legal_document_view import LegalDocumentAcceptView

# Customer-only legal document actions (require login)
urlpatterns = [
    path('<uuid:legal_document_id>/accept/', LegalDocumentAcceptView.as_view(), name='customer-legal-document-accept'),
]
