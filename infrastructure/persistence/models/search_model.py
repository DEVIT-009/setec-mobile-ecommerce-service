import uuid
from django.db import models
from infrastructure.persistence.models.ecom_user_model import EcomUser


class SearchHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(EcomUser, null=True, blank=True, on_delete=models.CASCADE, related_name='search_history')
    query = models.CharField(max_length=500)
    filters_json = models.JSONField(null=True, blank=True)
    result_count = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'search_history'
        constraints = [
            models.UniqueConstraint(fields=['user', 'query'], name='unique_user_query'),
        ]
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['query']),
        ]

    def __str__(self):
        return f"{self.user_id} — {self.query}"
