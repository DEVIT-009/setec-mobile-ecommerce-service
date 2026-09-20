from django.db import models
from infrastructure.persistence.models.shipment_model import Shipment
from shared.id_generator.id_generator import generate_shipment_event_id


class ShipmentEvent(models.Model):
    id = models.CharField(max_length=20, primary_key=True, editable=False)
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='events')
    status = models.CharField(max_length=20, choices=Shipment.STATUS_CHOICES)
    location = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    event_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'shipment_events'
        indexes = [
            models.Index(fields=['shipment']),
            models.Index(fields=['event_time']),
        ]

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_shipment_event_id()
        super().save(*args, **kwargs)


__all__ = ['ShipmentEvent']
