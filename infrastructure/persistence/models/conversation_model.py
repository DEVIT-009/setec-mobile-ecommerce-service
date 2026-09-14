import uuid
from django.db import models
from infrastructure.persistence.models.ecom_user_model import EcomUser
from infrastructure.persistence.models.store_model import Store
from infrastructure.persistence.models.order_model import Order


class Conversation(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('archived', 'Archived'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(EcomUser, on_delete=models.CASCADE, related_name='conversations')
    store = models.ForeignKey(Store, null=True, blank=True, on_delete=models.SET_NULL, related_name='conversations')
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL, related_name='conversations')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    last_message_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(EcomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(EcomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(EcomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    class Meta:
        db_table = 'conversations'
        indexes = [
            models.Index(fields=['customer']),
            models.Index(fields=['store']),
            models.Index(fields=['order']),
            models.Index(fields=['status']),
        ]


def __getattr__(name):
    if name == 'Message':
        from .message_model import Message
        return Message
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


__all__ = [
    'Conversation',
    'Message',
]
