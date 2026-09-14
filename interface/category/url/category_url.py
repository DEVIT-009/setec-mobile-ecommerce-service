from django.urls import path
from interface.category.view.category_admin_view import CategoryAdminView
from interface.category.view.category_public_view import CategoryPublicView

urlpatterns = [
    # ── Admin category routes ─────────────────────────────────────────────────
    # GET  /admin/categories/               -> list   (supports ?parent_id=)
    # POST /admin/categories/               -> create
    path('admin/categories/', CategoryAdminView.as_view({
        'get': 'list',
        'post': 'create',
    }), name='admin-category-list-create'),

    # GET /admin/categories/search/         -> retrieve by slug (?slug=)
    path('admin/categories/search/', CategoryAdminView.as_view({
        'get': 'retrieve_by_slug',
    }), name='admin-category-search'),

    # GET    /admin/categories/<uuid>/      -> retrieve by ID
    # PUT    /admin/categories/<uuid>/      -> full update
    # PATCH  /admin/categories/<uuid>/      -> partial update
    # DELETE /admin/categories/<uuid>/      -> soft delete
    path('admin/categories/<uuid:category_id>/', CategoryAdminView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy',
    }), name='admin-category-detail'),

    # ── Public category routes ────────────────────────────────────────────────
    # GET /public/categories/               -> list active (supports ?parent_id=)
    path('public/categories/', CategoryPublicView.as_view({
        'get': 'list',
    }), name='public-category-list'),

    # GET /public/categories/tree/          -> full active tree
    path('public/categories/tree/', CategoryPublicView.as_view({
        'get': 'tree',
    }), name='public-category-tree'),

    # GET /public/categories/search/        -> retrieve active by slug (?slug=)
    path('public/categories/search/', CategoryPublicView.as_view({
        'get': 'retrieve_by_slug',
    }), name='public-category-search'),

    # GET /public/categories/<uuid>/        -> retrieve active by ID
    path('public/categories/<uuid:category_id>/', CategoryPublicView.as_view({
        'get': 'retrieve',
    }), name='public-category-detail'),
]