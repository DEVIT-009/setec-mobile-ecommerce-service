from django.urls import path
from interface.order.view.order_admin_view import (
    AdminOrderCancelView, AdminOrderDetailView, AdminOrderFailedView,
    AdminOrderListView, AdminOrderProcessingView, AdminOrderStatusView,
)

# Admin order management endpoints — require authentication + admin role.
# GET   /api/v1/admin/orders/
# GET   /api/v1/admin/orders/<str:order_id>/
# PATCH /api/v1/admin/orders/<str:order_id>/status/
# PATCH /api/v1/admin/orders/<str:order_id>/processing
urlpatterns = [
    path('orders/', AdminOrderListView.as_view(), name='admin-order-list'),
    path('orders/<str:order_id>/', AdminOrderDetailView.as_view(), name='admin-order-detail'),
    path('orders/<str:order_id>/status/', AdminOrderStatusView.as_view(), name='admin-order-status'),
    path('orders/<str:order_id>/processing', AdminOrderProcessingView.as_view(), name='admin-order-processing'),
    path('orders/<str:order_id>/cancel', AdminOrderCancelView.as_view(), name='admin-order-cancel'),
    path('orders/<str:order_id>/failed', AdminOrderFailedView.as_view(), name='admin-order-failed'),
]
