from django.urls import path
from interface.tag.view.tag_view import TagPublicView

urlpatterns = [
    path('', TagPublicView.as_view({
        'get': 'list',
    }), name='tag-list'),
]
