from django.urls import path
from interface.order.view.order_view import (
    OrderListView, OrderDetailView, OrderCancelView,
    OrderStatusHistoryView, OrderShipmentsView,
)

urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),
    path('<str:order_id>/', OrderDetailView.as_view(), name='order-detail'),
    path('<str:order_id>/cancel/', OrderCancelView.as_view(), name='order-cancel'),
    path('<str:order_id>/status-history/', OrderStatusHistoryView.as_view(), name='order-status-history'),
    path('<str:order_id>/shipments/', OrderShipmentsView.as_view(), name='order-shipments'),
]
