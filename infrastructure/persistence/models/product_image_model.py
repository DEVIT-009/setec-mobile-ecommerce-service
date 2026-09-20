from django.db import models
from infrastructure.persistence.models.ecom_user_model import EcomUser
from infrastructure.persistence.models.product_model import Product
from shared.id_generator.id_generator import generate_product_image_id


class ProductImage(models.Model):
    id = models.CharField(max_length=20, primary_key=True, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image_url = models.TextField()
    alt_text = models.CharField(max_length=255, null=True, blank=True)
    sort_order = models.IntegerField(default=0)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(EcomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(EcomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(EcomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    class Meta:
        db_table = 'product_images'
        indexes = [models.Index(fields=['product'])]

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_product_image_id()
        super().save(*args, **kwargs)


__all__ = ['ProductImage']
