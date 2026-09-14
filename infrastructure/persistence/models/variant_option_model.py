import uuid
from django.db import models
from infrastructure.persistence.models.product_variant_model import ProductVariant


class VariantOption(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='options')
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    class Meta:
        db_table = 'variant_options'
        unique_together = [('product_variant', 'name')]


__all__ = ['VariantOption']
