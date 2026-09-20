from django.db import models
from infrastructure.persistence.models.product_model import Product
from infrastructure.persistence.models.tag_model import Tag


class ProductTag(models.Model):
    id = models.CharField(max_length=20, primary_key=True, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='product_tags')

    class Meta:
        db_table = 'product_tags'
        unique_together = [('product', 'tag')]
        indexes = [
            models.Index(fields=['product']),
            models.Index(fields=['tag']),
        ]

    def save(self, *args, **kwargs):
        if not self.id:
            from shared.id_generator.id_generator import generate_tag_id
            self.id = generate_tag_id()
        super().save(*args, **kwargs)


__all__ = ['ProductTag']
