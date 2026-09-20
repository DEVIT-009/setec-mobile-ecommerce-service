from django.db import models
from infrastructure.persistence.models.ecom_user_model import EcomUser
from infrastructure.persistence.models.store_model import Store
from infrastructure.persistence.models.category_model import Category
from shared.id_generator.id_generator import generate_product_id


class Product(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('out_of_stock', 'Out of Stock'),
    ]

    id = models.CharField(max_length=20, primary_key=True, editable=False)
    store = models.ForeignKey(Store, on_delete=models.RESTRICT, related_name='products')
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name='products')
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    base_price = models.DecimalField(max_digits=12, decimal_places=2)
    compare_at_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, default='USD')
    sku = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='draft')
    rating_average = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    rating_count = models.IntegerField(default=0)
    sold_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(EcomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(EcomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(EcomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    class Meta:
        db_table = 'products'
        unique_together = [('store', 'slug')]
        indexes = [
            models.Index(fields=['store']),
            models.Index(fields=['category']),
            models.Index(fields=['name']),
            models.Index(fields=['status']),
            models.Index(fields=['deleted_at']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_product_id()
        super().save(*args, **kwargs)


def __getattr__(name):
    if name == 'ProductImage':
        from .product_image_model import ProductImage
        return ProductImage
    if name == 'ProductVariant':
        from .product_variant_model import ProductVariant
        return ProductVariant
    if name == 'VariantOption':
        from .variant_option_model import VariantOption
        return VariantOption
    if name == 'Tag':
        from .tag_model import Tag
        return Tag
    if name == 'ProductTag':
        from .product_tag_model import ProductTag
        return ProductTag
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


__all__ = [
    'Product',
    'ProductImage',
    'ProductVariant',
    'VariantOption',
    'Tag',
    'ProductTag',
]
