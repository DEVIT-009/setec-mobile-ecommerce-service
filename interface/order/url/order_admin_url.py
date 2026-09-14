from django.urls import path
from interface.order.view.order_admin_view import (
    AdminOrderListView, AdminOrderDetailView, AdminOrderStatusView,
)

# Admin order management endpoints — require authentication + admin role.
# GET   /api/v1/admin/orders/
# GET   /api/v1/admin/orders/<uuid:order_id>/
# PATCH /api/v1/admin/orders/<uuid:order_id>/status/
urlpatterns = [
    path('orders/', AdminOrderListView.as_view(), name='admin-order-list'),
    path('orders/<uuid:order_id>/', AdminOrderDetailView.as_view(), name='admin-order-detail'),
    path('orders/<uuid:order_id>/status/', AdminOrderStatusView.as_view(), name='admin-order-status'),
]
