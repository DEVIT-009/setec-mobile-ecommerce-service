from django.core.management.base import BaseCommand
from infrastructure.persistence.models.role_model import Role
from infrastructure.persistence.models.permission_model import Permission, RoleHasPermission


class Command(BaseCommand):
    help = "Seed default roles and permissions into the database (idempotent — safe to re-run)."

    # ──────────────────────────────────────────────────────────────────────────
    # ROLES
    # ──────────────────────────────────────────────────────────────────────────
    ROLES = [
        {
            "name": "Customer",
            "slug": "customer",
            "description": "Regular storefront buyer. Can browse, shop, review, and manage their own account.",
        },
        {
            "name": "Admin",
            "slug": "admin",
            "description": "Platform administrator. Full catalog, order, and moderation access.",
        },
        {
            "name": "Support",
            "slug": "support",
            "description": "Customer support agent. Can view tickets, reply, and monitor conversations.",
        },
    ]

    # ──────────────────────────────────────────────────────────────────────────
    # PERMISSIONS
    # Grouped by domain for readability. Slug convention: <domain>.<action>
    # ──────────────────────────────────────────────────────────────────────────
    PERMISSIONS = [

        # ── Auth & Session ────────────────────────────────────────────────────
        {"name": "Auth: Logout",              "slug": "auth.logout"},
        {"name": "Auth: Refresh Token",       "slug": "auth.refresh"},
        {"name": "Auth: Verify Email",        "slug": "auth.verify_email"},
        {"name": "Auth: Verify Phone",        "slug": "auth.verify_phone"},
        {"name": "Auth: View Identity (Me)",  "slug": "auth.me"},

        # ── User Profile & Account ────────────────────────────────────────────
        {"name": "User: View Profile",                "slug": "user.profile.view"},
        {"name": "User: Update Profile",              "slug": "user.profile.update"},
        {"name": "User: View Extended Profile",       "slug": "user.profile.extended.view"},
        {"name": "User: Update Extended Profile",     "slug": "user.profile.extended.update"},
        {"name": "User: View Security Settings",      "slug": "user.security.view"},
        {"name": "User: Update Security Settings",    "slug": "user.security.update"},
        {"name": "User: View Sessions",               "slug": "user.sessions.view"},
        {"name": "User: Revoke Session",              "slug": "user.sessions.revoke"},
        {"name": "User: View Legal Acceptances",      "slug": "user.legal_acceptances.view"},

        # ── Addresses ─────────────────────────────────────────────────────────
        {"name": "Address: List",           "slug": "address.list"},
        {"name": "Address: Create",         "slug": "address.create"},
        {"name": "Address: View",           "slug": "address.view"},
        {"name": "Address: Update",         "slug": "address.update"},
        {"name": "Address: Delete",         "slug": "address.delete"},
        {"name": "Address: Set Default",    "slug": "address.set_default"},

        # ── Cart ──────────────────────────────────────────────────────────────
        {"name": "Cart: View",              "slug": "cart.view"},
        {"name": "Cart: Add Item",          "slug": "cart.item.add"},
        {"name": "Cart: Update Item",       "slug": "cart.item.update"},
        {"name": "Cart: Remove Item",       "slug": "cart.item.remove"},
        {"name": "Cart: Select All",        "slug": "cart.select_all"},
        {"name": "Cart: Checkout Preview",  "slug": "cart.checkout_preview"},

        # ── Orders ────────────────────────────────────────────────────────────
        {"name": "Order: List (Own)",           "slug": "order.list"},
        {"name": "Order: Place",                "slug": "order.create"},
        {"name": "Order: View (Own)",           "slug": "order.view"},
        {"name": "Order: Cancel (Own)",         "slug": "order.cancel"},
        {"name": "Order: View Status History",  "slug": "order.status_history.view"},
        {"name": "Order: View Shipments",       "slug": "order.shipments.view"},
        {"name": "Order: List All (Admin)",     "slug": "order.list.admin"},
        {"name": "Order: Update Status (Admin)","slug": "order.status.update"},

        # ── Shipments ─────────────────────────────────────────────────────────
        {"name": "Shipment: View",              "slug": "shipment.view"},
        {"name": "Shipment: View Events",       "slug": "shipment.events.view"},
        {"name": "Shipment: List All (Admin)",  "slug": "shipment.list.admin"},
        {"name": "Shipment: Update (Admin)",    "slug": "shipment.update"},

        # ── Favorites / Wishlist ──────────────────────────────────────────────
        {"name": "Favorite: List",      "slug": "favorite.list"},
        {"name": "Favorite: Add",       "slug": "favorite.add"},
        {"name": "Favorite: Remove",    "slug": "favorite.remove"},
        {"name": "Favorite: Check",     "slug": "favorite.check"},

        # ── Search History ────────────────────────────────────────────────────
        {"name": "Search History: List",            "slug": "search_history.list"},
        {"name": "Search History: Save",            "slug": "search_history.save"},
        {"name": "Search History: Clear All",       "slug": "search_history.clear_all"},
        {"name": "Search History: Delete Entry",    "slug": "search_history.delete"},

        # ── Reviews ───────────────────────────────────────────────────────────
        {"name": "Review: List Own",            "slug": "review.list.own"},
        {"name": "Review: Create",              "slug": "review.create"},
        {"name": "Review: Update (Own)",        "slug": "review.update"},
        {"name": "Review: Delete (Own)",        "slug": "review.delete"},
        {"name": "Review: List All (Admin)",    "slug": "review.list.admin"},
        {"name": "Review: Moderate (Admin)",    "slug": "review.moderate"},
        {"name": "Review: Delete (Admin)",      "slug": "review.delete.admin"},

        # ── Conversations & Messages ──────────────────────────────────────────
        {"name": "Conversation: List",          "slug": "conversation.list"},
        {"name": "Conversation: Start",         "slug": "conversation.create"},
        {"name": "Conversation: View",          "slug": "conversation.view"},
        {"name": "Conversation: Close",         "slug": "conversation.close"},
        {"name": "Message: List",               "slug": "message.list"},
        {"name": "Message: Send",               "slug": "message.send"},
        {"name": "Message: Mark Read",          "slug": "message.read"},

        # ── Notifications ─────────────────────────────────────────────────────
        {"name": "Notification: List",              "slug": "notification.list"},
        {"name": "Notification: Unread Count",      "slug": "notification.unread_count"},
        {"name": "Notification: Mark All Read",     "slug": "notification.read_all"},
        {"name": "Notification: Mark Single Read",  "slug": "notification.read"},
        {"name": "Notification: Delete",            "slug": "notification.delete"},
        {"name": "Notification: Broadcast (Admin)", "slug": "notification.broadcast"},

        # ── Support Tickets ───────────────────────────────────────────────────
        {"name": "Support Ticket: List",                    "slug": "support.ticket.list"},
        {"name": "Support Ticket: Create",                  "slug": "support.ticket.create"},
        {"name": "Support Ticket: View",                    "slug": "support.ticket.view"},
        {"name": "Support Ticket: Update",                  "slug": "support.ticket.update"},
        {"name": "Support Ticket: List Messages",           "slug": "support.ticket.messages.list"},
        {"name": "Support Ticket: Reply",                   "slug": "support.ticket.messages.reply"},

        # ── Legal Documents ───────────────────────────────────────────────────
        {"name": "Legal Document: Accept",          "slug": "legal.accept"},
        {"name": "Legal Document: List (Admin)",    "slug": "legal.list.admin"},
        {"name": "Legal Document: Create (Admin)",  "slug": "legal.create"},
        {"name": "Legal Document: View (Admin)",    "slug": "legal.view.admin"},
        {"name": "Legal Document: Update (Admin)",  "slug": "legal.update"},
        {"name": "Legal Document: Delete (Admin)",  "slug": "legal.delete"},

        # ── Uploads ───────────────────────────────────────────────────────────
        {"name": "Upload: Request Cloudinary Signature",    "slug": "upload.signature"},
        {"name": "Upload: Confirm Asset",                   "slug": "upload.confirm"},

        # ── Categories (Admin) ────────────────────────────────────────────────
        {"name": "Category: List (Admin)",      "slug": "category.list.admin"},
        {"name": "Category: Create",            "slug": "category.create"},
        {"name": "Category: View (Admin)",      "slug": "category.view.admin"},
        {"name": "Category: Update",            "slug": "category.update"},
        {"name": "Category: Delete",            "slug": "category.delete"},

        # ── Stores (Admin) ────────────────────────────────────────────────────
        {"name": "Store: List (Admin)",     "slug": "store.list.admin"},
        {"name": "Store: Create",           "slug": "store.create"},
        {"name": "Store: View (Admin)",     "slug": "store.view.admin"},
        {"name": "Store: Update",           "slug": "store.update"},
        {"name": "Store: Delete",           "slug": "store.delete"},

        # ── Products (Admin) ──────────────────────────────────────────────────
        {"name": "Product: List (Admin)",   "slug": "product.list.admin"},
        {"name": "Product: Create",         "slug": "product.create"},
        {"name": "Product: View (Admin)",   "slug": "product.view.admin"},
        {"name": "Product: Update",         "slug": "product.update"},
        {"name": "Product: Delete",         "slug": "product.delete"},

        # ── Product Variants (Admin) ──────────────────────────────────────────
        {"name": "Product Variant: List (Admin)",    "slug": "product.variant.list.admin"},
        {"name": "Product Variant: Create",          "slug": "product.variant.create"},
        {"name": "Product Variant: View (Admin)",    "slug": "product.variant.view.admin"},
        {"name": "Product Variant: Update",          "slug": "product.variant.update"},
        {"name": "Product Variant: Delete",          "slug": "product.variant.delete"},

        # ── Product Variant Options (Admin) ───────────────────────────────────
        {"name": "Variant Option: List (Admin)",    "slug": "product.variant_option.list.admin"},
        {"name": "Variant Option: Create",          "slug": "product.variant_option.create"},
        {"name": "Variant Option: View (Admin)",    "slug": "product.variant_option.view.admin"},
        {"name": "Variant Option: Update",          "slug": "product.variant_option.update"},
        {"name": "Variant Option: Delete",          "slug": "product.variant_option.delete"},

        # ── Tags (Admin) ──────────────────────────────────────────────────────
        {"name": "Tag: List (Admin)",   "slug": "tag.list.admin"},
        {"name": "Tag: Create",         "slug": "tag.create"},
        {"name": "Tag: View (Admin)",   "slug": "tag.view.admin"},
        {"name": "Tag: Update",         "slug": "tag.update"},
        {"name": "Tag: Delete",         "slug": "tag.delete"},
    ]

    # ──────────────────────────────────────────────────────────────────────────
    # ROLE → PERMISSIONS MAPPING
    # ──────────────────────────────────────────────────────────────────────────
    ROLE_PERMISSIONS = {

        # ── customer ──────────────────────────────────────────────────────────
        # Everything under /api/v1/auth/, /api/v1/users/me/, /api/v1/addresses/,
        # /api/v1/cart/, /api/v1/orders/, /api/v1/shipments/, /api/v1/favorites/,
        # /api/v1/search-history/, /api/v1/reviews/ (own), /api/v1/conversations/,
        # /api/v1/notifications/, /api/v1/support/tickets/, /api/v1/legal-documents/,
        # /api/v1/uploads/
        "customer": [
            # Auth & session
            "auth.logout",
            "auth.refresh",
            "auth.verify_email",
            "auth.verify_phone",
            "auth.me",
            # User profile
            "user.profile.view",
            "user.profile.update",
            "user.profile.extended.view",
            "user.profile.extended.update",
            "user.security.view",
            "user.security.update",
            "user.sessions.view",
            "user.sessions.revoke",
            "user.legal_acceptances.view",
            # Addresses
            "address.list",
            "address.create",
            "address.view",
            "address.update",
            "address.delete",
            "address.set_default",
            # Cart
            "cart.view",
            "cart.item.add",
            "cart.item.update",
            "cart.item.remove",
            "cart.select_all",
            "cart.checkout_preview",
            # Orders
            "order.list",
            "order.create",
            "order.view",
            "order.cancel",
            "order.status_history.view",
            "order.shipments.view",
            # Shipments
            "shipment.view",
            "shipment.events.view",
            # Favorites
            "favorite.list",
            "favorite.add",
            "favorite.remove",
            "favorite.check",
            # Search history
            "search_history.list",
            "search_history.save",
            "search_history.clear_all",
            "search_history.delete",
            # Reviews (own)
            "review.list.own",
            "review.create",
            "review.update",
            "review.delete",
            # Conversations & messages
            "conversation.list",
            "conversation.create",
            "conversation.view",
            "conversation.close",
            "message.list",
            "message.send",
            "message.read",
            # Notifications
            "notification.list",
            "notification.unread_count",
            "notification.read_all",
            "notification.read",
            "notification.delete",
            # Support tickets
            "support.ticket.list",
            "support.ticket.create",
            "support.ticket.view",
            "support.ticket.update",
            "support.ticket.messages.list",
            "support.ticket.messages.reply",
            # Legal
            "legal.accept",
            # Uploads
            "upload.signature",
            "upload.confirm",
        ],

        # ── support ───────────────────────────────────────────────────────────
        # Auth session management + read/reply on tickets + conversation monitoring
        "support": [
            # Auth & session
            "auth.logout",
            "auth.refresh",
            "auth.verify_email",
            "auth.verify_phone",
            "auth.me",
            # User profile (own)
            "user.profile.view",
            "user.profile.update",
            "user.profile.extended.view",
            "user.profile.extended.update",
            "user.security.view",
            "user.security.update",
            "user.sessions.view",
            "user.sessions.revoke",
            "user.legal_acceptances.view",
            # Notifications
            "notification.list",
            "notification.unread_count",
            "notification.read_all",
            "notification.read",
            "notification.delete",
            # Conversations (monitoring)
            "conversation.list",
            "conversation.view",
            "conversation.close",
            "message.list",
            "message.send",
            "message.read",
            # Support tickets (full access)
            "support.ticket.list",
            "support.ticket.view",
            "support.ticket.update",
            "support.ticket.messages.list",
            "support.ticket.messages.reply",
            # Uploads
            "upload.signature",
            "upload.confirm",
        ],

        # ── admin ─────────────────────────────────────────────────────────────
        # Full platform access: all customer permissions + all admin-only actions
        "admin": [
            # Auth & session
            "auth.logout",
            "auth.refresh",
            "auth.verify_email",
            "auth.verify_phone",
            "auth.me",
            # User profile (own)
            "user.profile.view",
            "user.profile.update",
            "user.profile.extended.view",
            "user.profile.extended.update",
            "user.security.view",
            "user.security.update",
            "user.sessions.view",
            "user.sessions.revoke",
            "user.legal_acceptances.view",
            # Shipments (admin read + update)
            "shipment.view",
            "shipment.events.view",
            "shipment.list.admin",
            "shipment.update",
            # Orders (admin full)
            "order.list.admin",
            "order.view",
            "order.status_history.view",
            "order.shipments.view",
            "order.status.update",
            # Reviews (admin moderation)
            "review.list.admin",
            "review.moderate",
            "review.delete.admin",
            # Conversations & messages (admin monitoring)
            "conversation.list",
            "conversation.view",
            "conversation.close",
            "message.list",
            "message.send",
            "message.read",
            # Notifications
            "notification.list",
            "notification.unread_count",
            "notification.read_all",
            "notification.read",
            "notification.delete",
            "notification.broadcast",
            # Support tickets (full admin)
            "support.ticket.list",
            "support.ticket.view",
            "support.ticket.update",
            "support.ticket.messages.list",
            "support.ticket.messages.reply",
            # Legal documents (admin full)
            "legal.list.admin",
            "legal.create",
            "legal.view.admin",
            "legal.update",
            "legal.delete",
            # Uploads
            "upload.signature",
            "upload.confirm",
            # Categories (admin full)
            "category.list.admin",
            "category.create",
            "category.view.admin",
            "category.update",
            "category.delete",
            # Stores (admin full)
            "store.list.admin",
            "store.create",
            "store.view.admin",
            "store.update",
            "store.delete",
            # Products (admin full)
            "product.list.admin",
            "product.create",
            "product.view.admin",
            "product.update",
            "product.delete",
            # Product variants
            "product.variant.list.admin",
            "product.variant.create",
            "product.variant.view.admin",
            "product.variant.update",
            "product.variant.delete",
            # Variant options
            "product.variant_option.list.admin",
            "product.variant_option.create",
            "product.variant_option.view.admin",
            "product.variant_option.update",
            "product.variant_option.delete",
            # Tags
            "tag.list.admin",
            "tag.create",
            "tag.view.admin",
            "tag.update",
            "tag.delete",
        ],
    }

    # ──────────────────────────────────────────────────────────────────────────
    # HANDLE
    # ──────────────────────────────────────────────────────────────────────────
    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("\n=== Seeding Roles ==="))
        self._seed_roles()

        self.stdout.write(self.style.MIGRATE_HEADING("\n=== Seeding Permissions ==="))
        self._seed_permissions()

        self.stdout.write(self.style.MIGRATE_HEADING("\n=== Assigning Permissions to Roles ==="))
        self._assign_permissions()

        self.stdout.write(self.style.SUCCESS("\n✅ Roles and permissions seeded successfully!\n"))

    def _seed_roles(self):
        for r in self.ROLES:
            role, created = Role.objects.update_or_create(
                slug=r["slug"],
                defaults={"name": r["name"], "description": r.get("description", "")},
            )
            action = "Created" if created else "Updated"
            self.stdout.write(f"  [{action}] Role: {role.slug}")

    def _seed_permissions(self):
        for p in self.PERMISSIONS:
            perm, created = Permission.objects.update_or_create(
                slug=p["slug"],
                defaults={"name": p["name"]},
            )
            action = "Created" if created else "Updated"
            self.stdout.write(f"  [{action}] Permission: {perm.slug}")

    def _assign_permissions(self):
        for role_slug, perm_slugs in self.ROLE_PERMISSIONS.items():
            try:
                role = Role.objects.get(slug=role_slug)
            except Role.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"  [SKIP] Role '{role_slug}' not found — skipping.")
                )
                continue

            assigned = 0
            for perm_slug in perm_slugs:
                try:
                    perm = Permission.objects.get(slug=perm_slug)
                except Permission.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f"  [WARN] Permission '{perm_slug}' not found — skipping.")
                    )
                    continue

                _, created = RoleHasPermission.objects.get_or_create(role=role, permission=perm)
                if created:
                    assigned += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f"  [{role_slug}] {assigned} new permission(s) assigned "
                    f"({len(perm_slugs)} total in mapping)"
                )
            )
