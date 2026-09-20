from django.db import models
from infrastructure.persistence.models.ecom_user_model import EcomUser
from shared.id_generator.id_generator import generate_cart_id


class Cart(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('checked_out', 'Checked Out'),
        ('abandoned', 'Abandoned'),
    ]

    id = models.CharField(max_length=20, primary_key=True, editable=False)
    user = models.ForeignKey(EcomUser, on_delete=models.CASCADE, related_name='carts')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(EcomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(EcomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(EcomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    class Meta:
        db_table = 'carts'
        indexes = [models.Index(fields=['user'])]

    def __str__(self):
        return f"Cart({self.user_id}, {self.status})"

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_cart_id()
        super().save(*args, **kwargs)


def __getattr__(name):
    if name == 'CartItem':
        from .cart_item_model import CartItem
        return CartItem
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


__all__ = [
    'Cart',
    'CartItem',
]
