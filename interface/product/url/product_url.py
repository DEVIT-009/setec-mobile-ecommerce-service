from django.urls import path

from interface.product.view.product_admin_view import ProductAdminView
from interface.product.view.product_public_view import ProductPublicView

urlpatterns = [
    # ── Admin routes — prefix: admin/products/ ────────────────────────────────
    path('admin/products/', ProductAdminView.as_view({'get': 'list', 'post': 'create'}), name='admin-product-list-create'),
    path('admin/products/<str:product_id>/', ProductAdminView.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='admin-product-detail'),

    # ── Public routes — prefix: public/products/ ─────────────────────────────
    path('public/products/', ProductPublicView.as_view({'get': 'list'}), name='public-product-list'),
    path('public/products/tags/', ProductPublicView.as_view({'get': 'list_tags'}), name='public-product-tags'),
    path('public/products/slug/<slug:store_slug>/<slug:product_slug>/', ProductPublicView.as_view({'get': 'retrieve_by_store_slug'}), name='public-product-slug-detail'),
    path('public/products/<str:product_id>/', ProductPublicView.as_view({'get': 'retrieve'}), name='public-product-detail'),
    path('public/products/<str:product_id>/images/', ProductPublicView.as_view({'get': 'images'}), name='public-product-images'),
    path('public/products/<str:product_id>/variants/', ProductPublicView.as_view({'get': 'variants'}), name='public-product-variants'),
    path('public/products/<str:product_id>/reviews/', ProductPublicView.as_view({'get': 'reviews'}), name='public-product-reviews'),
    path('public/products/<str:product_id>/favorite/', ProductPublicView.as_view({'get': 'favorite_state'}), name='public-product-favorite-state'),
]
