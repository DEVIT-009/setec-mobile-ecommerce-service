from django.urls import path

from interface.product.view.variant_option_admin_view import VariantOptionAdminView
from interface.product.view.variant_option_public_view import VariantOptionPublicView

urlpatterns = [
    # ── Public routes — prefix: api/v1/public/product/variant-options/ ─────────
    path('public/product/variant-options/', VariantOptionPublicView.as_view({'get': 'list'}), name='public-variant-option-list'),
    path('public/product/variant-options/<uuid:option_id>/', VariantOptionPublicView.as_view({'get': 'retrieve'}), name='public-variant-option-detail'),

    # ── Admin routes — prefix: api/v1/admin/product/variant-options/ ───────────
    path('admin/product/variant-options/', VariantOptionAdminView.as_view({'get': 'list', 'post': 'create'}), name='admin-variant-option-list-create'),
    path('admin/product/variant-options/<uuid:option_id>/', VariantOptionAdminView.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='admin-variant-option-detail'),
]
