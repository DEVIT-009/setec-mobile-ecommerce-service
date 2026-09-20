from django.db import models
from infrastructure.persistence.models.product_variant_model import ProductVariant
from shared.id_generator.id_generator import generate_option_id


class VariantOption(models.Model):
    id = models.CharField(max_length=20, primary_key=True, editable=False)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='options')
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    class Meta:
        db_table = 'variant_options'
        unique_together = [('product_variant', 'name')]

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_option_id()
        super().save(*args, **kwargs)


__all__ = ['VariantOption']
