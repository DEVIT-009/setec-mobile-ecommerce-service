from django.db import models
from infrastructure.persistence.models.ecom_user_model import EcomUser
from infrastructure.persistence.models.legal_document_model import LegalDocument
from shared.id_generator.id_generator import generate_legal_acceptance_id


class LegalAcceptance(models.Model):
    id = models.CharField(max_length=20, primary_key=True, editable=False)
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

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_legal_acceptance_id()
        super().save(*args, **kwargs)


__all__ = ['LegalAcceptance']
