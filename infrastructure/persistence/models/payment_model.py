from django.db import models

from infrastructure.persistence.models.ecom_user_model import EcomUser
from infrastructure.persistence.models.order_model import Order
from shared.id_generator.id_generator import generate_payment_batch_id, generate_payment_id


class PaymentBatch(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('succeeded', 'Succeeded'),
        ('partially_refunded', 'Partially Refunded'),
        ('refunded', 'Refunded'),
    ]

    id = models.CharField(max_length=20, primary_key=True, editable=False)
    user = models.ForeignKey(EcomUser, on_delete=models.RESTRICT, related_name='payment_batches')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    provider = models.CharField(max_length=40, default='internal_mock')
    provider_reference = models.CharField(max_length=100, null=True, blank=True, unique=True)
    idempotency_key = models.CharField(max_length=128, unique=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    refunded_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payment_batches'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_payment_batch_id()
        super().save(*args, **kwargs)


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('succeeded', 'Succeeded'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]

    id = models.CharField(max_length=20, primary_key=True, editable=False)
    batch = models.ForeignKey(
        PaymentBatch,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='payments',
    )
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment_record')
    user = models.ForeignKey(EcomUser, on_delete=models.RESTRICT, related_name='payments')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    provider = models.CharField(max_length=40, default='internal_mock')
    provider_reference = models.CharField(max_length=100, null=True, blank=True, unique=True)
    idempotency_key = models.CharField(max_length=128, unique=True)
    failure_reason = models.TextField(null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    refunded_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payments'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_payment_id()
        super().save(*args, **kwargs)


__all__ = ['Payment', 'PaymentBatch']
