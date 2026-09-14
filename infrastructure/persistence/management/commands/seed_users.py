from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from infrastructure.persistence.models.ecom_user_model import EcomUser, UserProfile, UserSecuritySettings


class Command(BaseCommand):
    help = "Seed initial test users (Customer, Admin, Support) with credentials from frontend integration guide."

    def handle(self, *args, **options):
        seed_users = [
            {
                "email": "customer@example.com",
                "password": "Password123!",
                "first_name": "Jane",
                "last_name": "Customer",
                "phone_number": "+12345678901",
                "role": "customer",
                "status": "active",
            },
            {
                "email": "admin@example.com",
                "password": "AdminSecret123!",
                "first_name": "Admin",
                "last_name": "User",
                "phone_number": "+12345678902",
                "role": "admin",
                "status": "active",
            },
            {
                "email": "support@example.com",
                "password": "SupportSecret123!",
                "first_name": "Support",
                "last_name": "Agent",
                "phone_number": "+12345678903",
                "role": "support",
                "status": "active",
            },
        ]

        now = timezone.now()

        for u in seed_users:
            user, created = EcomUser.objects.update_or_create(
                email=u["email"].lower(),
                defaults={
                    "password_hash": make_password(u["password"]),
                    "first_name": u["first_name"],
                    "last_name": u["last_name"],
                    "phone_number": u["phone_number"],
                    "role": u["role"],
                    "status": u["status"],
                    "email_verified_at": now,
                    "deleted_at": None,
                },
            )

            UserProfile.objects.get_or_create(user=user)
            UserSecuritySettings.objects.get_or_create(user=user)

            action = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"[{action}] {u['role'].capitalize()} user: {u['email']}"))

        self.stdout.write(self.style.SUCCESS("Seed users successfully provisioned!"))
