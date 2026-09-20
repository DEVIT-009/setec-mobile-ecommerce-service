from django.db import models
from infrastructure.persistence.models.ecom_user_model import EcomUser
from infrastructure.persistence.models.order_model import Order
from shared.id_generator.id_generator import generate_order_status_log_id


class OrderStatusHistory(models.Model):
    id = models.CharField(max_length=20, primary_key=True, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history')
    from_status = models.CharField(max_length=15, null=True, blank=True)
    to_status = models.CharField(max_length=15)
    changed_by = models.ForeignKey(EcomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order_status_history'
        indexes = [models.Index(fields=['order'])]

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_order_status_log_id()
        super().save(*args, **kwargs)


__all__ = ['OrderStatusHistory']
