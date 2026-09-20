from django.urls import path
from interface.tag.view.tag_admin_view import TagAdminView

urlpatterns = [
    path('tags/', TagAdminView.as_view({
        'get': 'list',
        'post': 'create',
    }), name='admin-tag-list-create'),
    path('tags/<str:tag_id>/', TagAdminView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy',
    }), name='admin-tag-detail'),
]
