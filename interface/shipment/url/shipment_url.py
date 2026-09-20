from django.urls import path
from interface.shipment.view.shipment_view import ShipmentDetailView, ShipmentEventsView

urlpatterns = [
    path('<str:shipment_id>/', ShipmentDetailView.as_view(), name='shipment-detail'),
    path('<str:shipment_id>/events/', ShipmentEventsView.as_view(), name='shipment-events'),
]
