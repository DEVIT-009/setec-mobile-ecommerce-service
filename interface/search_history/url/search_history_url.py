from django.urls import path
from interface.search_history.view.search_history_view import SearchHistoryListView, SearchHistoryDetailView

urlpatterns = [
    path('', SearchHistoryListView.as_view(), name='search-history-list'),
    path('<uuid:search_id>/', SearchHistoryDetailView.as_view(), name='search-history-detail'),
]
