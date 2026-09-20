from django.db import models
from infrastructure.persistence.models.ecom_user_model import EcomUser
from shared.id_generator.id_generator import generate_category_id


class Category(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    id = models.CharField(max_length=20, primary_key=True, editable=False)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children')
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    icon_url = models.TextField(null=True, blank=True)
    image_url = models.TextField(null=True, blank=True)
    sort_order = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(EcomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(EcomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(EcomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    class Meta:
        db_table = 'categories'
        indexes = [
            models.Index(fields=['parent']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_category_id()
        super().save(*args, **kwargs)
