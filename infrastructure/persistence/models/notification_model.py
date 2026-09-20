from django.db import models
from infrastructure.persistence.models.ecom_user_model import EcomUser
from shared.id_generator.id_generator import generate_notification_id


class Notification(models.Model):
    TYPE_CHOICES = [
        ('order', 'Order'),
        ('promotion', 'Promotion'),
        ('message', 'Message'),
        ('system', 'System'),
        ('security', 'Security'),
    ]
    STATUS_CHOICES = [
        ('queued', 'Queued'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ]

    id = models.CharField(max_length=20, primary_key=True, editable=False)
    user = models.ForeignKey(EcomUser, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=15, choices=TYPE_CHOICES)
    title = models.CharField(max_length=255)
    body = models.TextField(null=True, blank=True)
    data = models.JSONField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='queued')
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'notifications'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['type']),
            models.Index(fields=['status']),
            models.Index(fields=['read_at']),
        ]

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_notification_id()
        super().save(*args, **kwargs)
