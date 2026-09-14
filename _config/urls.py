from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),

    # Legacy auth endpoint
    re_path(r'^api/v1/legacy-auth/?', include('shared.security.auth_url')),

    # Category endpoints (Admin, Public, Compatibility)
    path('api/v1/', include('interface.category.url.category_url')),

    # Store endpoints (Admin, Public, Compatibility)
    path('api/v1/', include('interface.store.url.store_url')),

    # Product endpoints (Admin + Public) — all routes live in one unified URL file
    path('api/v1/', include('interface.product.url.product_url')),

    # Product Variant endpoints (Admin + Public)
    path('api/v1/', include('interface.product.url.product_variant_url')),

    # Product Variant Option endpoints (Admin + Public)
    path('api/v1/', include('interface.product.url.variant_option_url')),

    # ──────────────────────────────────────────────────────────────────────────
    # Public read-only resources  →  /api/v1/public/<resource>/
    # No authentication required (guests may access freely)
    # ──────────────────────────────────────────────────────────────────────────
    path('api/v1/public/', include('interface.tag.url.tag_public_url')),
    path('api/v1/public/reviews/', include('interface.review.url.review_url')),
    path('api/v1/public/legal-documents/', include('interface.legal_document.url.legal_document_url')),

    # ──────────────────────────────────────────────────────────────────────────
    # Admin management resources  →  /api/v1/admin/<resource>/
    # Require: authenticated JWT + "admin" role  →  401 / 403 otherwise
    # ──────────────────────────────────────────────────────────────────────────
    path('api/v1/admin/', include('interface.tag.url.tag_admin_url')),

    path('api/v1/admin/', include('interface.order.url.order_admin_url')),
    path('api/v1/admin/', include('interface.shipment.url.shipment_admin_url')),
    path('api/v1/admin/', include('interface.review.url.review_admin_url')),
    path('api/v1/admin/', include('interface.notification.url.notification_admin_url')),
    path('api/v1/admin/', include('interface.support_ticket.url.support_ticket_admin_url')),
    path('api/v1/admin/', include('interface.legal_document.url.legal_document_admin_url')),

    # ──────────────────────────────────────────────────────────────────────────
    # Auth endpoints  →  /api/v1/auth/
    # Mixed: register/login/forgot-password are public; logout/me require JWT
    # ──────────────────────────────────────────────────────────────────────────
    re_path(r'^api/v1/auth/?', include('interface.auth.url.auth_url')),

    # ──────────────────────────────────────────────────────────────────────────
    # Public home feed  →  /api/v1/home/
    # No auth required; user_id is optional (personalises feed when present)
    # ──────────────────────────────────────────────────────────────────────────
    re_path(r'^api/v1/home/?', include('interface.home.url.home_url')),

    # ──────────────────────────────────────────────────────────────────────────
    # Customer-only resources  →  /api/v1/customer/<feature>/
    # ALL routes here require a valid customer JWT  →  401 / 403 otherwise
    # ──────────────────────────────────────────────────────────────────────────
    path('api/v1/customer/users/', include('interface.user.url.user_url')),
    path('api/v1/customer/addresses/', include('interface.address.url.address_url')),
    path('api/v1/customer/orders/', include('interface.order.url.order_url')),
    path('api/v1/customer/shipments/', include('interface.shipment.url.shipment_url')),
    path('api/v1/customer/search-history/', include('interface.search_history.url.search_history_url')),
    path('api/v1/customer/favorites/', include('interface.favorite.url.favorite_url')),
    path('api/v1/customer/cart/', include('interface.cart.url.cart_url')),
    path('api/v1/customer/conversations/', include('interface.conversation.url.conversation_url')),
    path('api/v1/customer/messages/', include('interface.conversation.url.message_url')),
    path('api/v1/customer/notifications/', include('interface.notification.url.notification_url')),
    path('api/v1/customer/support/', include('interface.support_ticket.url.support_ticket_url')),
    path('api/v1/customer/legal-documents/', include('interface.legal_document.url.legal_document_customer_url')),
    path('api/v1/customer/uploads/', include('interface.upload.url.upload_url')),

    # ──────────────────────────────────────────────────────────────────────────
    # Backward-compatibility aliases for Flutter clients
    # These map the OLD public URLs to the same views as /public/* routes.
    # The sub-url files use root-relative paths (e.g. '' and '<slug:slug>/')
    # so we must include them with the full prefix path.
    # TODO: Remove once Flutter is updated to use /api/v1/public/* paths.
    # ──────────────────────────────────────────────────────────────────────────
    # NOTE: The legacy api/v1/products/ backward-compat alias has been removed.
    # product_url.py now contains fully-prefixed routes (public/products/, admin/products/).
    # Flutter clients should migrate to /api/v1/public/products/ and /api/v1/admin/products/.
    path('api/v1/tags/', include('interface.tag.url.tag_url')),
    re_path(r'^api/v1/reviews/?', include('interface.review.url.review_url')),

]
