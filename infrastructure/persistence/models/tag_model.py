from django.db import models
from shared.id_generator.id_generator import generate_tag_id


class Tag(models.Model):
    id = models.CharField(max_length=20, primary_key=True, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=120, unique=True)

    class Meta:
        db_table = 'tags'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_tag_id()
        super().save(*args, **kwargs)


__all__ = ['Tag']
