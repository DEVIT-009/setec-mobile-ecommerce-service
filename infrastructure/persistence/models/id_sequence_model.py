"""
Database-backed sequence table used by the ID generator.

A single row per *sequence_key* stores the last-used integer value.
The ID generator increments this inside a SELECT FOR UPDATE transaction
to guarantee uniqueness under concurrent load.
"""
from django.db import models


class IdSequence(models.Model):
    sequence_key  = models.CharField(max_length=50, primary_key=True)
    current_value = models.BigIntegerField(default=0)

    class Meta:
        db_table = "id_sequences"

    def __str__(self):
        return f"{self.sequence_key}={self.current_value}"


__all__ = ["IdSequence"]
