import uuid
from django.db import models


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=120, unique=True)

    class Meta:
        db_table = 'tags'

    def __str__(self):
        return self.name


__all__ = ['Tag']
