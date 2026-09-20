from django.db import models
from infrastructure.persistence.models.ecom_user_model import EcomUser
from infrastructure.persistence.models.product_model import Product


class Favorite(models.Model):
    # Numeric BigAutoField PK per the ID strategy spec
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(EcomUser, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'favorites'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['product']),
        ]
