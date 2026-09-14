import uuid
from django.db import models
from infrastructure.persistence.models.ecom_user_model import EcomUser
from infrastructure.persistence.models.legal_document_model import LegalDocument


class LegalAcceptance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(EcomUser, on_delete=models.CASCADE, related_name='legal_acceptances')
    legal_document = models.ForeignKey(LegalDocument, on_delete=models.RESTRICT, related_name='acceptances')
    accepted_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = 'legal_acceptances'
        unique_together = [('user', 'legal_document')]
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['legal_document']),
        ]


__all__ = ['LegalAcceptance']
