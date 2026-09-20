from django.db import models
from infrastructure.persistence.models.ecom_user_model import EcomUser
from infrastructure.persistence.models.order_model import Order
from shared.id_generator.id_generator import generate_shipment_id


class Shipment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('packed', 'Packed'),
        ('in_transit', 'In Transit'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
        ('returned', 'Returned'),
    ]

    id = models.CharField(max_length=20, primary_key=True, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='shipments')
    carrier_name = models.CharField(max_length=100, null=True, blank=True)
    tracking_number = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(EcomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(EcomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(EcomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    class Meta:
        db_table = 'shipments'
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['status']),
            models.Index(fields=['tracking_number']),
        ]

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_shipment_id()
        super().save(*args, **kwargs)


def __getattr__(name):
    if name == 'ShipmentEvent':
        from .shipment_event_model import ShipmentEvent
        return ShipmentEvent
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


__all__ = [
    'Shipment',
    'ShipmentEvent',
]
