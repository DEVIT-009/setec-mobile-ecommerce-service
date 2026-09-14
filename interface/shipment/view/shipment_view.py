from rest_framework.views import APIView
from rest_framework.request import Request

from application.shipment.factory.shipment_service_factory import shipment_service_factory
from shared.responseutils.response_handler import ResponseHandler
from shared.metadata_handler.request_header_utillity import metadata_handler


class ShipmentDetailView(APIView):
    @metadata_handler(required_user_id=True)
    def get(self, request: Request, shipment_id=None, metadata=None):
        service = shipment_service_factory()
        return ResponseHandler.api_success(service.get_detail(str(shipment_id)))


class ShipmentEventsView(APIView):
    @metadata_handler(required_user_id=True)
    def get(self, request: Request, shipment_id=None, metadata=None):
        service = shipment_service_factory()
        return ResponseHandler.api_success(service.get_events(str(shipment_id)))
