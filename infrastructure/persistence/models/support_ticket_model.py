from django.db import models
from infrastructure.persistence.models.ecom_user_model import EcomUser
from infrastructure.persistence.models.order_model import Order
from shared.id_generator.id_generator import generate_ticket_id


class SupportTicket(models.Model):
    CATEGORY_CHOICES = [
        ('order', 'Order'),
        ('payment', 'Payment'),
        ('delivery', 'Delivery'),
        ('account', 'Account'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    id = models.CharField(max_length=20, primary_key=True, editable=False)
    user = models.ForeignKey(EcomUser, on_delete=models.CASCADE, related_name='support_tickets')
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL, related_name='support_tickets')
    subject = models.CharField(max_length=255)
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES, default='other')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(EcomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(EcomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(EcomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    class Meta:
        db_table = 'support_tickets'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['order']),
            models.Index(fields=['status']),
        ]

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_ticket_id()
        super().save(*args, **kwargs)


__all__ = ['SupportTicket']
