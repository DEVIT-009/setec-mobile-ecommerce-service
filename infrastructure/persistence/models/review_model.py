from django.db import models
from infrastructure.persistence.models.ecom_user_model import EcomUser
from infrastructure.persistence.models.product_model import Product
from infrastructure.persistence.models.product_variant_model import ProductVariant
from infrastructure.persistence.models.order_item_model import OrderItem
from shared.id_generator.id_generator import generate_review_id


class Review(models.Model):
    id = models.CharField(max_length=20, primary_key=True, editable=False)
    user = models.ForeignKey(EcomUser, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    product_variant = models.ForeignKey(ProductVariant, null=True, blank=True, on_delete=models.SET_NULL, related_name='reviews')
    order_item = models.ForeignKey(OrderItem, null=True, blank=True, on_delete=models.SET_NULL, related_name='reviews')
    rating = models.IntegerField()
    title = models.CharField(max_length=255, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    is_verified_purchase = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'reviews'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['product']),
            models.Index(fields=['rating']),
        ]

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_review_id()
        super().save(*args, **kwargs)


__all__ = ['Review']
