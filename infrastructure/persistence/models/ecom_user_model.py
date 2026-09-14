import uuid
from django.db import models


class EcomUser(models.Model):
    USER_ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('seller', 'Seller'),
        ('admin', 'Admin'),
        ('support', 'Support'),
    ]
    USER_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('blocked', 'Blocked'),
        ('pending_verification', 'Pending Verification'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=32, unique=True, null=True, blank=True)
    password_hash = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    avatar_url = models.TextField(null=True, blank=True)
    role = models.CharField(max_length=20, choices=USER_ROLE_CHOICES, default='customer')
    status = models.CharField(max_length=30, choices=USER_STATUS_CHOICES, default='pending_verification')
    email_verified_at = models.DateTimeField(null=True, blank=True)
    phone_verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='created_users')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='updated_users')
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='deleted_users')

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['role']),
            models.Index(fields=['status']),
            models.Index(fields=['deleted_at']),
        ]

    def __str__(self):
        return self.email

    @property
    def is_active(self):
        return self.status == 'active'

    @property
    def full_name(self):
        return f"{self.first_name or ''} {self.last_name or ''}".strip()


def __getattr__(name):
    if name == 'UserProfile':
        from .user_profile_model import UserProfile
        return UserProfile
    if name in ('UserAddress', 'Address'):
        from .user_address_model import UserAddress
        return UserAddress
    if name == 'UserSecuritySettings':
        from .user_security_settings_model import UserSecuritySettings
        return UserSecuritySettings
    if name == 'UserSession':
        from .user_session_model import UserSession
        return UserSession
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


__all__ = [
    'EcomUser',
    'UserProfile',
    'UserAddress',
    'UserSecuritySettings',
    'UserSession',
]
