import uuid

from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class UserManager(models.Manager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = email.strip().lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password or "")
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(email, password, **extra_fields)


class User(models.Model):
    id = models.CharField(primary_key=True, max_length=50, default=uuid.uuid4, editable=False)
    last_login = models.DateTimeField(null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=250, unique=True)
    password = models.CharField(max_length=255)

    bio = models.CharField(max_length=200, null=True, blank=True)
    avatar = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    phone_code = models.CharField(max_length=10, null=True, blank=True)

    status = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_by = models.CharField(max_length=64, null=True, blank=True)
    updated_by = models.CharField(max_length=64, null=True, blank=True)
    deleted_by = models.CharField(max_length=64, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        db_table = "legacy_users"

    def __str__(self):
        return self.email

    @property
    def is_active(self):
        return self.status

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def set_password(self, raw_password):
        self.password = make_password(raw_password or "")

    def check_password(self, raw_password):
        return check_password(raw_password or "", self.password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False
