from django.urls import path
from interface.shipment.view.shipment_admin_view import AdminShipmentListView, AdminShipmentDetailView

# Admin shipment management endpoints — require authentication + admin role.
# GET   /api/v1/admin/shipments/
# GET   /api/v1/admin/shipments/<uuid:shipment_id>/
# PATCH /api/v1/admin/shipments/<uuid:shipment_id>/
urlpatterns = [
    path('shipments/', AdminShipmentListView.as_view(), name='admin-shipment-list'),
    path('shipments/<uuid:shipment_id>/', AdminShipmentDetailView.as_view(), name='admin-shipment-detail'),
]
