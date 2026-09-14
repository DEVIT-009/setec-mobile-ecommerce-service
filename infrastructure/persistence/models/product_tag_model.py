import uuid
from django.db import models
from infrastructure.persistence.models.product_model import Product
from infrastructure.persistence.models.tag_model import Tag


class ProductTag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='product_tags')

    class Meta:
        db_table = 'product_tags'
        unique_together = [('product', 'tag')]
        indexes = [
            models.Index(fields=['product']),
            models.Index(fields=['tag']),
        ]


__all__ = ['ProductTag']
