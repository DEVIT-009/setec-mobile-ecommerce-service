from django.urls import path

from interface.product.view.product_variant_admin_view import ProductVariantAdminView
from interface.product.view.product_variant_public_view import ProductVariantPublicView

urlpatterns = [
    # ── Public routes — prefix: api/v1/public/product/variants/ ───────────────
    path('public/product/variants/', ProductVariantPublicView.as_view({'get': 'list'}), name='public-product-variant-list'),
    path('public/product/variants/<str:variant_id>/', ProductVariantPublicView.as_view({'get': 'retrieve'}), name='public-product-variant-detail'),

    # ── Admin routes — prefix: api/v1/admin/product/variants/ ─────────────────
    path('admin/product/variants/', ProductVariantAdminView.as_view({'get': 'list', 'post': 'create'}), name='admin-product-variant-list-create'),
    path('admin/product/variants/<str:variant_id>/', ProductVariantAdminView.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='admin-product-variant-detail'),
]
