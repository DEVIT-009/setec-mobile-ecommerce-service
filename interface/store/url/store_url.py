from django.urls import path
from interface.store.view.store_admin_view import StoreAdminView
from interface.store.view.store_public_view import StorePublicView

urlpatterns = [
    # ── Admin store routes ────────────────────────────────────────────────────
    # GET  /admin/stores/                  -> list (supports ?page=&page_size=)
    # POST /admin/stores/                  -> create
    path('admin/stores/', StoreAdminView.as_view({
        'get': 'list',
        'post': 'create',
    }), name='admin-store-list-create'),

    # GET /admin/stores/search/            -> retrieve by slug (?slug=)
    path('admin/stores/search/', StoreAdminView.as_view({
        'get': 'retrieve_by_slug',
    }), name='admin-store-search'),

    # GET    /admin/stores/<uuid>/         -> retrieve by ID
    # PUT    /admin/stores/<uuid>/         -> full update
    # PATCH  /admin/stores/<uuid>/         -> partial update
    # DELETE /admin/stores/<uuid>/         -> soft delete
    path('admin/stores/<uuid:store_id>/', StoreAdminView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy',
    }), name='admin-store-detail'),

    # ── Public store routes ───────────────────────────────────────────────────
    # GET /public/stores/                  -> list active (paginated)
    path('public/stores/', StorePublicView.as_view({
        'get': 'list',
    }), name='public-store-list'),

    # GET /public/stores/search/           -> retrieve active by slug (?slug=)
    path('public/stores/search/', StorePublicView.as_view({
        'get': 'retrieve_by_slug',
    }), name='public-store-search'),

    # GET /public/stores/search/products/  -> list products by store slug (?slug=)
    path('public/stores/search/products/', StorePublicView.as_view({
        'get': 'products_by_slug',
    }), name='public-store-search-products'),

    # GET /public/stores/<uuid>/           -> retrieve active by ID
    path('public/stores/<uuid:store_id>/', StorePublicView.as_view({
        'get': 'retrieve',
    }), name='public-store-detail'),

    # GET /public/stores/<uuid>/products/  -> list products by store UUID ID
    path('public/stores/<uuid:store_id>/products/', StorePublicView.as_view({
        'get': 'products',
    }), name='public-store-products'),
]
