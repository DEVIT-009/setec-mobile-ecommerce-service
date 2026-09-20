from django.urls import path
from interface.search_history.view.search_history_customer_view import SearchHistoryCustomerView

urlpatterns = [
    path('', SearchHistoryCustomerView.as_view({'get': 'list', 'post': 'create', 'delete': 'clear'}), name='customer-search-history-list'),
    path('<uuid:search_id>/', SearchHistoryCustomerView.as_view({'delete': 'destroy'}), name='customer-search-history-detail'),
]
