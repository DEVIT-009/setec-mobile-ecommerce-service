from django.db import models
from infrastructure.persistence.models.ecom_user_model import EcomUser
from infrastructure.persistence.models.support_ticket_model import SupportTicket
from shared.id_generator.id_generator import generate_ticket_message_id


class SupportTicketMessage(models.Model):
    id = models.CharField(max_length=20, primary_key=True, editable=False)
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='ticket_messages')
    sender = models.ForeignKey(EcomUser, on_delete=models.CASCADE, related_name='support_messages')
    body = models.TextField()
    attachment_url = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'support_ticket_messages'
        indexes = [
            models.Index(fields=['ticket']),
            models.Index(fields=['sender']),
        ]

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_ticket_message_id()
        super().save(*args, **kwargs)


__all__ = ['SupportTicketMessage']
