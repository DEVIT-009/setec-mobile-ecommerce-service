import uuid
from django.db import models


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=120, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'roles'

    def __str__(self):
        return self.slug


class UserRole(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        'EcomUser',
        on_delete=models.CASCADE,
        related_name='user_roles',
        db_column='user_id',
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name='user_roles',
        db_column='role_id',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_roles'
        unique_together = [('user', 'role')]

    def __str__(self):
        return f'{self.user_id} -> {self.role.slug}'
