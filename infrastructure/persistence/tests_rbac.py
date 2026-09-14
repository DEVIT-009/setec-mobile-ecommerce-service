"""
RBAC + Route access test suite.

Verifies:
1. Public endpoints are accessible to guests, customer JWT, and admin JWT.
2. Admin endpoints return 401 for guests and 403 for customers.
3. Admin endpoints are accessible to admin JWT.
4. Users with multiple roles (e.g. "customer,admin") can access admin endpoints.
5. Inactive/deleted records are excluded from public endpoints.
6. Soft-deleted records are excluded from admin endpoints.
"""
import uuid
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth.hashers import make_password

from infrastructure.persistence.models.ecom_user_model import EcomUser
from infrastructure.persistence.models.category_model import Category
from shared.security.jwt_util import JwtUtil


def _make_jwt(user: EcomUser, roles=None) -> str:
    """Generate a JWT for a given user with an optional roles override."""
    return JwtUtil.generate_token_for_ecom(user, roles=roles)


class PublicEndpointAccessTest(TestCase):
    """
    Public endpoints must return HTTP 200 for:
    - Guest (no Authorization header)
    - Customer JWT
    - Admin JWT
    And must exclude inactive/deleted records.
    """

    def setUp(self):
        self.customer = EcomUser.objects.create(
            email="rbac_customer@example.com",
            password_hash=make_password("Password123!"),
            role="customer",
            status="active",
        )
        self.admin_user = EcomUser.objects.create(
            email="rbac_admin@example.com",
            password_hash=make_password("Password123!"),
            role="admin",
            status="active",
        )
        # Active category — should appear in public listing
        self.active_cat = Category.objects.create(
            name="Active Category",
            slug="active-category",
            status="active",
        )
        # Inactive category — must NOT appear in public listing
        self.inactive_cat = Category.objects.create(
            name="Inactive Category",
            slug="inactive-category",
            status="inactive",
        )
        # Soft-deleted category — must NOT appear anywhere
        from django.utils import timezone
        self.deleted_cat = Category.objects.create(
            name="Deleted Category",
            slug="deleted-category",
            status="active",
            deleted_at=timezone.now(),
        )

        self.customer_jwt = _make_jwt(self.customer)
        self.admin_jwt = _make_jwt(self.admin_user)

    def test_public_categories_guest(self):
        """GET /api/v1/public/categories/ → 200 without token."""
        resp = self.client.get("/api/v1/public/categories/")
        self.assertEqual(resp.status_code, 200, msg=resp.content)

    def test_public_categories_customer_jwt(self):
        """GET /api/v1/public/categories/ → 200 with customer JWT."""
        resp = self.client.get(
            "/api/v1/public/categories/",
            HTTP_AUTHORIZATION=f"Bearer {self.customer_jwt}",
        )
        self.assertEqual(resp.status_code, 200, msg=resp.content)

    def test_public_categories_admin_jwt(self):
        """GET /api/v1/public/categories/ → 200 with admin JWT."""
        resp = self.client.get(
            "/api/v1/public/categories/",
            HTTP_AUTHORIZATION=f"Bearer {self.admin_jwt}",
        )
        self.assertEqual(resp.status_code, 200, msg=resp.content)

    def test_public_categories_excludes_inactive_and_deleted(self):
        """
        Public category list must only return active, non-deleted records.
        """
        resp = self.client.get("/api/v1/public/categories/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        # The exact shape depends on ResponseHandler, but we check slugs in body
        body_str = resp.content.decode()
        self.assertIn("active-category", body_str)
        self.assertNotIn("inactive-category", body_str)
        self.assertNotIn("deleted-category", body_str)

    def test_public_stores_guest(self):
        """GET /api/v1/public/stores/ → 200 without token."""
        resp = self.client.get("/api/v1/public/stores/")
        self.assertEqual(resp.status_code, 200, msg=resp.content)

    def test_public_products_guest(self):
        """GET /api/v1/public/products/ → 200 without token."""
        resp = self.client.get("/api/v1/public/products/")
        self.assertEqual(resp.status_code, 200, msg=resp.content)

    def test_public_tags_guest(self):
        """GET /api/v1/public/tags/ → 200 without token."""
        resp = self.client.get("/api/v1/public/tags/")
        self.assertEqual(resp.status_code, 200, msg=resp.content)


class AdminEndpointAccessTest(TestCase):
    """
    Admin endpoints must return:
    - 401 for guests (no JWT)
    - 403 for customers (JWT with customer role)
    - 200 for admins (JWT with admin role)
    And must exclude soft-deleted records while including active + inactive.
    """

    def setUp(self):
        self.customer = EcomUser.objects.create(
            email="rbac2_customer@example.com",
            password_hash=make_password("Password123!"),
            role="customer",
            status="active",
        )
        self.admin_user = EcomUser.objects.create(
            email="rbac2_admin@example.com",
            password_hash=make_password("Password123!"),
            role="admin",
            status="active",
        )
        self.customer_jwt = _make_jwt(self.customer)
        self.admin_jwt = _make_jwt(self.admin_user)

    def test_admin_categories_guest_returns_401(self):
        """GET /api/v1/admin/categories/ → 401 without token."""
        resp = self.client.get("/api/v1/admin/categories/")
        self.assertEqual(resp.status_code, 401, msg=resp.content)

    def test_admin_categories_customer_returns_403(self):
        """GET /api/v1/admin/categories/ → 403 with customer JWT."""
        resp = self.client.get(
            "/api/v1/admin/categories/",
            HTTP_AUTHORIZATION=f"Bearer {self.customer_jwt}",
        )
        self.assertEqual(resp.status_code, 403, msg=resp.content)

    def test_admin_categories_admin_returns_200(self):
        """GET /api/v1/admin/categories/ → 200 with admin JWT."""
        resp = self.client.get(
            "/api/v1/admin/categories/",
            HTTP_AUTHORIZATION=f"Bearer {self.admin_jwt}",
        )
        self.assertEqual(resp.status_code, 200, msg=resp.content)

    def test_admin_orders_guest_returns_401(self):
        """GET /api/v1/admin/orders/ → 401 without token."""
        resp = self.client.get("/api/v1/admin/orders/")
        self.assertEqual(resp.status_code, 401, msg=resp.content)

    def test_admin_orders_customer_returns_403(self):
        """GET /api/v1/admin/orders/ → 403 with customer JWT."""
        resp = self.client.get(
            "/api/v1/admin/orders/",
            HTTP_AUTHORIZATION=f"Bearer {self.customer_jwt}",
        )
        self.assertEqual(resp.status_code, 403, msg=resp.content)

    def test_admin_notifications_guest_returns_401(self):
        """GET /api/v1/admin/notifications/ → 401 without token."""
        resp = self.client.get("/api/v1/admin/notifications/")
        self.assertEqual(resp.status_code, 401, msg=resp.content)

    def test_admin_notifications_customer_returns_403(self):
        """GET /api/v1/admin/notifications/ → 403 with customer JWT."""
        resp = self.client.get(
            "/api/v1/admin/notifications/",
            HTTP_AUTHORIZATION=f"Bearer {self.customer_jwt}",
        )
        self.assertEqual(resp.status_code, 403, msg=resp.content)

    def test_admin_support_tickets_guest_returns_401(self):
        """GET /api/v1/admin/support/tickets/ → 401 without token."""
        resp = self.client.get("/api/v1/admin/support/tickets/")
        self.assertEqual(resp.status_code, 401, msg=resp.content)

    def test_admin_support_tickets_customer_returns_403(self):
        """GET /api/v1/admin/support/tickets/ → 403 with customer JWT."""
        resp = self.client.get(
            "/api/v1/admin/support/tickets/",
            HTTP_AUTHORIZATION=f"Bearer {self.customer_jwt}",
        )
        self.assertEqual(resp.status_code, 403, msg=resp.content)

    def test_admin_legal_documents_guest_returns_401(self):
        """GET /api/v1/admin/legal-documents/ → 401 without token."""
        resp = self.client.get("/api/v1/admin/legal-documents/")
        self.assertEqual(resp.status_code, 401, msg=resp.content)

    def test_admin_stores_guest_returns_401(self):
        """GET /api/v1/admin/stores/ → 401 without token."""
        resp = self.client.get("/api/v1/admin/stores/")
        self.assertEqual(resp.status_code, 401, msg=resp.content)

    def test_admin_products_customer_returns_403(self):
        """GET /api/v1/admin/products/ → 403 with customer JWT."""
        resp = self.client.get(
            "/api/v1/admin/products/",
            HTTP_AUTHORIZATION=f"Bearer {self.customer_jwt}",
        )
        self.assertEqual(resp.status_code, 403, msg=resp.content)

    def test_admin_reviews_customer_returns_403(self):
        """GET /api/v1/admin/reviews/ → 403 with customer JWT."""
        resp = self.client.get(
            "/api/v1/admin/reviews/",
            HTTP_AUTHORIZATION=f"Bearer {self.customer_jwt}",
        )
        self.assertEqual(resp.status_code, 403, msg=resp.content)

    def test_admin_category_crud(self):
        """POST, PUT, PATCH, DELETE /api/v1/admin/categories/ with admin JWT."""
        # 1. Create
        create_resp = self.client.post(
            "/api/v1/admin/categories/",
            data={
                "name": "Smartphones",
                "slug": "smartphones",
                "sort_order": 1,
                "status": "active",
            },
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.admin_jwt}",
        )
        self.assertEqual(create_resp.status_code, 201, msg=create_resp.content)
        cat_id = create_resp.json()["data"]["id"]
        self.assertIsNotNone(cat_id)
        self.assertEqual(create_resp.json()["data"]["slug"], "smartphones")

        # 2. Duplicate slug returns 400
        dup_resp = self.client.post(
            "/api/v1/admin/categories/",
            data={
                "name": "Another Phone",
                "slug": "smartphones",
            },
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.admin_jwt}",
        )
        self.assertEqual(dup_resp.status_code, 400)

        # 3. GET by slug and by category_id
        get_slug_resp = self.client.get(
            "/api/v1/admin/categories/smartphones/",
            HTTP_AUTHORIZATION=f"Bearer {self.admin_jwt}",
        )
        self.assertEqual(get_slug_resp.status_code, 200)
        self.assertEqual(get_slug_resp.json()["data"]["id"], cat_id)

        get_id_resp = self.client.get(
            f"/api/v1/admin/categories/{cat_id}/",
            HTTP_AUTHORIZATION=f"Bearer {self.admin_jwt}",
        )
        self.assertEqual(get_id_resp.status_code, 200)
        self.assertEqual(get_id_resp.json()["data"]["slug"], "smartphones")

        # 3b. Verify PUT, PATCH, DELETE with slug are rejected with 404 (ID only allowed)
        put_by_slug = self.client.put(
            "/api/v1/admin/categories/smartphones/",
            data={
                "name": "Should Fail",
                "slug": "smartphones",
                "sort_order": 2,
                "status": "active",
            },
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.admin_jwt}",
        )
        self.assertEqual(put_by_slug.status_code, 404)

        patch_by_slug = self.client.patch(
            "/api/v1/admin/categories/smartphones/",
            data={"name": "Should Fail"},
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.admin_jwt}",
        )
        self.assertEqual(patch_by_slug.status_code, 404)

        del_by_slug = self.client.delete(
            "/api/v1/admin/categories/smartphones/",
            HTTP_AUTHORIZATION=f"Bearer {self.admin_jwt}",
        )
        self.assertEqual(del_by_slug.status_code, 404)

        # 4. PUT with category_id
        put_resp = self.client.put(
            f"/api/v1/admin/categories/{cat_id}/",
            data={
                "name": "Flagship Smartphones",
                "slug": "smartphones",
                "sort_order": 2,
                "status": "active",
            },
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.admin_jwt}",
        )
        self.assertEqual(put_resp.status_code, 200)
        self.assertEqual(put_resp.json()["data"]["name"], "Flagship Smartphones")

        # 5. PATCH with category_id
        patch_resp = self.client.patch(
            f"/api/v1/admin/categories/{cat_id}/",
            data={"name": "Smartphones & Tablets"},
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.admin_jwt}",
        )
        self.assertEqual(patch_resp.status_code, 200)
        self.assertEqual(patch_resp.json()["data"]["name"], "Smartphones & Tablets")

        # 6. DELETE with category_id
        del_resp = self.client.delete(
            f"/api/v1/admin/categories/{cat_id}/",
            HTTP_AUTHORIZATION=f"Bearer {self.admin_jwt}",
        )
        self.assertEqual(del_resp.status_code, 204)

        # 7. Verify 404 after soft delete
        get_after_del = self.client.get(
            f"/api/v1/admin/categories/{cat_id}/",
            HTTP_AUTHORIZATION=f"Bearer {self.admin_jwt}",
        )
        self.assertEqual(get_after_del.status_code, 404)

        # 8. Verify non-existent category id or slug (e.g. esdfghjkc) returns 404, not 405
        put_404 = self.client.put(
            "/api/v1/admin/categories/esdfghjkc/",
            data={
                "name": "Non-existent",
                "slug": "non-existent",
                "sort_order": 1,
                "status": "active",
            },
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.admin_jwt}",
        )
        self.assertEqual(put_404.status_code, 404)

        put_empty_404 = self.client.put(
            "/api/v1/admin/categories/esdfghjkc/",
            data={},
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.admin_jwt}",
        )
        self.assertEqual(put_empty_404.status_code, 404)

        patch_404 = self.client.patch(
            "/api/v1/admin/categories/esdfghjkc/",
            data={"name": "Non-existent"},
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.admin_jwt}",
        )
        self.assertEqual(patch_404.status_code, 404)

        delete_404 = self.client.delete(
            "/api/v1/admin/categories/esdfghjkc/",
            HTTP_AUTHORIZATION=f"Bearer {self.admin_jwt}",
        )
        self.assertEqual(delete_404.status_code, 404)

        get_404 = self.client.get(
            "/api/v1/admin/categories/esdfghjkc/",
            HTTP_AUTHORIZATION=f"Bearer {self.admin_jwt}",
        )
        self.assertEqual(get_404.status_code, 404)

    def test_legal_document_latest_public(self):
        """GET /api/v1/legal-documents/{type}/latest/ returns 404 or 200 without 500 AttributeError."""
        resp = self.client.get("/api/v1/legal-documents/terms/latest/")
        # If none exist, should return 404, not 500
        self.assertIn(resp.status_code, [200, 404])


class MultiRoleAccessTest(TestCase):
    """
    Users with multiple roles (e.g. role="customer,admin" in the JWT) must
    be able to access admin endpoints.
    """

    def setUp(self):
        # User stored in DB with role="customer" but will get a multi-role JWT
        self.multi_role_user = EcomUser.objects.create(
            email="rbac_multirole@example.com",
            password_hash=make_password("Password123!"),
            role="customer",  # DB value — the JWT overrides this for RBAC checks
            status="active",
        )
        # Generate a JWT explicitly with both roles (comma-separated)
        self.multi_role_jwt = _make_jwt(
            self.multi_role_user, roles=["customer", "admin"]
        )

    def test_multi_role_user_can_access_admin_categories(self):
        """
        A user with ['customer', 'admin'] in their JWT role claim must get
        HTTP 200 on admin endpoints.
        """
        resp = self.client.get(
            "/api/v1/admin/categories/",
            HTTP_AUTHORIZATION=f"Bearer {self.multi_role_jwt}",
        )
        self.assertEqual(resp.status_code, 200, msg=resp.content)

    def test_multi_role_user_can_access_admin_orders(self):
        """Admin orders list must be accessible with multi-role JWT."""
        resp = self.client.get(
            "/api/v1/admin/orders/",
            HTTP_AUTHORIZATION=f"Bearer {self.multi_role_jwt}",
        )
        self.assertEqual(resp.status_code, 200, msg=resp.content)

    def test_multi_role_user_still_accesses_public_routes(self):
        """Multi-role users must still access public endpoints."""
        resp = self.client.get(
            "/api/v1/public/categories/",
            HTTP_AUTHORIZATION=f"Bearer {self.multi_role_jwt}",
        )
        self.assertEqual(resp.status_code, 200, msg=resp.content)


class BackwardCompatibilityAliasTest(TestCase):
    """
    Old Flutter-facing URLs must still work (backward compat aliases).
    """

    def test_old_categories_url_still_works(self):
        """GET /api/v1/categories/ must still return 200 for guests."""
        resp = self.client.get("/api/v1/categories/")
        self.assertEqual(resp.status_code, 200, msg=resp.content)

    def test_old_stores_url_still_works(self):
        """GET /api/v1/stores/ must still return 200 for guests."""
        resp = self.client.get("/api/v1/stores/")
        self.assertEqual(resp.status_code, 200, msg=resp.content)

    def test_old_products_url_still_works(self):
        """GET /api/v1/products/ must still return 200 for guests."""
        resp = self.client.get("/api/v1/products/")
        self.assertEqual(resp.status_code, 200, msg=resp.content)

    def test_old_tags_url_still_works(self):
        """GET /api/v1/tags/ must still return 200 for guests."""
        resp = self.client.get("/api/v1/tags/")
        self.assertEqual(resp.status_code, 200, msg=resp.content)
