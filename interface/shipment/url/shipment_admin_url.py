from django.urls import path
from interface.shipment.view.shipment_admin_view import (
    AdminOrderShipmentCreateView,
    AdminShipmentDetailView,
    AdminShipmentCheckpointView,
    AdminShipmentHandoffView,
    AdminShipmentListView,
    AdminShipmentPackedView,
    AdminShipmentOutForDeliveryView,
)

# Admin shipment management endpoints — require authentication + admin role.
# GET   /api/v1/admin/shipments/
# GET   /api/v1/admin/shipments/<str:shipment_id>/
# PATCH /api/v1/admin/shipments/<str:shipment_id>/
urlpatterns = [
    path('orders/<str:order_id>/shipments', AdminOrderShipmentCreateView.as_view(), name='admin-order-shipment-create'),
    path('shipments/', AdminShipmentListView.as_view(), name='admin-shipment-list'),
    path('shipments/<str:shipment_id>/', AdminShipmentDetailView.as_view(), name='admin-shipment-detail'),
    path('shipments/<str:shipment_id>/packed', AdminShipmentPackedView.as_view(), name='admin-shipment-packed'),
    path('shipments/<str:shipment_id>/handoff', AdminShipmentHandoffView.as_view(), name='admin-shipment-handoff'),
    path('shipments/<str:shipment_id>/events', AdminShipmentCheckpointView.as_view(), name='admin-shipment-checkpoint'),
    path('shipments/<str:shipment_id>/out-for-delivery', AdminShipmentOutForDeliveryView.as_view(), name='admin-shipment-out-for-delivery'),
]
