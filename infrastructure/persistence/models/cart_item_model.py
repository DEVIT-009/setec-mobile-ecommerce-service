import uuid
from django.db import models
from infrastructure.persistence.models.ecom_user_model import EcomUser
from infrastructure.persistence.models.cart_model import Cart
from infrastructure.persistence.models.product_model import Product
from infrastructure.persistence.models.product_variant_model import ProductVariant


class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.RESTRICT, related_name='cart_items')
    product_variant = models.ForeignKey(ProductVariant, null=True, blank=True, on_delete=models.RESTRICT, related_name='cart_items')
    quantity = models.IntegerField()
    unit_price_snapshot = models.DecimalField(max_digits=12, decimal_places=2)
    is_selected = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(EcomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(EcomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(EcomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    class Meta:
        db_table = 'cart_items'
        indexes = [
            models.Index(fields=['cart']),
            models.Index(fields=['product']),
        ]


__all__ = ['CartItem']
