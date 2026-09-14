from django.urls import path
from interface.tag.view.tag_view import TagPublicView

urlpatterns = [
    path('tags/', TagPublicView.as_view({
        'get': 'list',
    }), name='public-tag-list'),
]
