from django.db import models


class Permission(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=120, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'permissions'

    def __str__(self):
        return self.slug


class RoleHasPermission(models.Model):
    id = models.AutoField(primary_key=True)
    role = models.ForeignKey(
        'Role',
        on_delete=models.CASCADE,
        related_name='role_permissions',
        db_column='role_id',
    )
    permission = models.ForeignKey(
        Permission,
        on_delete=models.CASCADE,
        related_name='role_permissions',
        db_column='permission_id',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'role_has_permissions'
        unique_together = [('role', 'permission')]

    def __str__(self):
        return f'{self.role.slug} -> {self.permission.slug}'
