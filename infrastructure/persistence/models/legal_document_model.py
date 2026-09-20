from django.db import models
from infrastructure.persistence.models.ecom_user_model import EcomUser
from shared.id_generator.id_generator import generate_legal_document_id


class LegalDocument(models.Model):
    TYPE_CHOICES = [
        ('terms', 'Terms'),
        ('privacy', 'Privacy'),
        ('refund_policy', 'Refund Policy'),
        ('shipping_policy', 'Shipping Policy'),
    ]
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    # legdoc-NN  (2-digit sequence, e.g. legdoc-01)
    id = models.CharField(max_length=12, primary_key=True, editable=False)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=255)
    version = models.CharField(max_length=50)
    content = models.TextField()
    published_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(EcomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(EcomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(EcomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    class Meta:
        db_table = 'legal_documents'
        unique_together = [('type', 'version')]
        indexes = [
            models.Index(fields=['type']),
            models.Index(fields=['status']),
        ]

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_legal_document_id()
        super().save(*args, **kwargs)


__all__ = ['LegalDocument']
