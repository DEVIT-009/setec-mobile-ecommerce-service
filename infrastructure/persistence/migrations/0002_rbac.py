# Migration: Multi-role RBAC — adds roles, user_roles, permissions, role_has_permissions
# and removes the single 'role' column from users.

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persistence', '0001_initial'),
    ]

    operations = [
        # -----------------------------------------------------------------
        # 1. Create the roles table
        # -----------------------------------------------------------------
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.CharField(max_length=120, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'db_table': 'roles'},
        ),

        # -----------------------------------------------------------------
        # 2. Create the permissions table
        # -----------------------------------------------------------------
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.CharField(max_length=120, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'db_table': 'permissions'},
        ),

        # -----------------------------------------------------------------
        # 3. Create the user_roles junction table
        # -----------------------------------------------------------------
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                (
                    'user',
                    models.ForeignKey(
                        db_column='user_id',
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='user_roles',
                        to='persistence.ecomuser',
                    ),
                ),
                (
                    'role',
                    models.ForeignKey(
                        db_column='role_id',
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='user_roles',
                        to='persistence.role',
                    ),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'db_table': 'user_roles'},
        ),
        migrations.AddConstraint(
            model_name='userrole',
            constraint=models.UniqueConstraint(fields=['user', 'role'], name='uq_user_role'),
        ),

        # -----------------------------------------------------------------
        # 4. Create the role_has_permissions junction table
        # -----------------------------------------------------------------
        migrations.CreateModel(
            name='RoleHasPermission',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                (
                    'role',
                    models.ForeignKey(
                        db_column='role_id',
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='role_permissions',
                        to='persistence.role',
                    ),
                ),
                (
                    'permission',
                    models.ForeignKey(
                        db_column='permission_id',
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='role_permissions',
                        to='persistence.permission',
                    ),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'db_table': 'role_has_permissions'},
        ),
        migrations.AddConstraint(
            model_name='roleHasPermission',
            constraint=models.UniqueConstraint(fields=['role', 'permission'], name='uq_role_permission'),
        ),

        # -----------------------------------------------------------------
        # 5. Remove the old single-role column from users
        # -----------------------------------------------------------------
        migrations.RemoveIndex(
            model_name='ecomuser',
            name='users_role_0ace22_idx',
        ),
        migrations.RemoveField(
            model_name='ecomuser',
            name='role',
        ),
    ]
