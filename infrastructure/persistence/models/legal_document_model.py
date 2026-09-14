import uuid
from django.db import models
from infrastructure.persistence.models.ecom_user_model import EcomUser


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

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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


__all__ = ['LegalDocument']
