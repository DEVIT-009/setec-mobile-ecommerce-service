from django.db import models
from infrastructure.persistence.models.ecom_user_model import EcomUser
from infrastructure.persistence.models.conversation_model import Conversation
from shared.id_generator.id_generator import generate_message_id


class Message(models.Model):
    TYPE_CHOICES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('system', 'System'),
    ]

    id = models.CharField(max_length=20, primary_key=True, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(EcomUser, on_delete=models.CASCADE, related_name='sent_messages')
    message_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='text')
    body = models.TextField(null=True, blank=True)
    attachment_url = models.TextField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'messages'
        indexes = [
            models.Index(fields=['conversation']),
            models.Index(fields=['sender']),
            models.Index(fields=['created_at']),
        ]

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_message_id()
        super().save(*args, **kwargs)


__all__ = ['Message']
