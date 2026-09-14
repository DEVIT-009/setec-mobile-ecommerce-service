import uuid
from django.db import models
from infrastructure.persistence.models.ecom_user_model import EcomUser


class UserAddress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(EcomUser, on_delete=models.CASCADE, related_name='addresses')
    label = models.CharField(max_length=100, null=True, blank=True)
    recipient_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=32)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120, null=True, blank=True)
    postal_code = models.CharField(max_length=32, null=True, blank=True)
    country_code = models.CharField(max_length=2)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(EcomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(EcomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(EcomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    class Meta:
        db_table = 'user_addresses'
        indexes = [models.Index(fields=['user'])]

    def __str__(self):
        return f"{self.recipient_name} - {self.city}"


Address = UserAddress
__all__ = ['UserAddress', 'Address']
