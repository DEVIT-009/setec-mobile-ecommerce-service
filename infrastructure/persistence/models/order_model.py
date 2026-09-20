from django.db import models
from infrastructure.persistence.models.ecom_user_model import EcomUser
from infrastructure.persistence.models.user_address_model import UserAddress
from infrastructure.persistence.models.store_model import Store
from shared.id_generator.id_generator import generate_order_id


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('paid', 'Paid'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]

    # The formatted ID IS the order identifier (ord-YYYYMMDD-NNNN).
    # No separate order_number field is needed.
    id = models.CharField(max_length=30, primary_key=True, editable=False)
    user = models.ForeignKey(EcomUser, on_delete=models.RESTRICT, related_name='orders')
    store = models.ForeignKey(Store, on_delete=models.RESTRICT, related_name='orders')
    shipping_address = models.ForeignKey(UserAddress, null=True, blank=True, on_delete=models.SET_NULL, related_name='orders')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    subtotal_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    shipping_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default='USD')
    placed_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(EcomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(EcomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(EcomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    class Meta:
        db_table = 'orders'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['store']),
            models.Index(fields=['status']),
            models.Index(fields=['placed_at']),
        ]

    def __str__(self):
        return self.id

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_order_id()
        super().save(*args, **kwargs)


def __getattr__(name):
    if name == 'OrderItem':
        from .order_item_model import OrderItem
        return OrderItem
    if name == 'OrderStatusHistory':
        from .order_status_history_model import OrderStatusHistory
        return OrderStatusHistory
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


__all__ = [
    'Order',
    'OrderItem',
    'OrderStatusHistory',
]
