from django.urls import path
from interface.favorite.view.favorite_view import FavoriteListView, FavoriteDeleteView

urlpatterns = [
    path('', FavoriteListView.as_view(), name='favorite-list'),
    path('<uuid:product_id>/', FavoriteDeleteView.as_view(), name='favorite-delete'),
]
