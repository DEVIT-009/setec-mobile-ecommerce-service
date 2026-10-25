from rest_framework.views import APIView
from rest_framework.request import Request

from application.shipment.factory.shipment_service_factory import shipment_service_factory
from interface.shipment.serializer.request.shipment_request import ConfirmDeliveryRequest
from shared.responseutils.response_handler import ResponseHandler
from shared.metadata_handler.request_header_utillity import metadata_handler


class ShipmentDetailView(APIView):
    @metadata_handler(required_user_id=True)
    def get(self, request: Request, shipment_id=None, metadata=None):
        service = shipment_service_factory()
        return ResponseHandler.api_success(service.get_detail(str(shipment_id), metadata.user_id))


class ShipmentEventsView(APIView):
    @metadata_handler(required_user_id=True)
    def get(self, request: Request, shipment_id=None, metadata=None):
        service = shipment_service_factory()
        return ResponseHandler.api_success(service.get_events(str(shipment_id), metadata.user_id))


class ShipmentConfirmDeliveryView(APIView):
    @metadata_handler(required_user_id=True)
    def post(self, request: Request, shipment_id=None, metadata=None):
        serializer = ConfirmDeliveryRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = shipment_service_factory()
        shipment = service.confirm_delivery(
            shipment_id=str(shipment_id),
            user_id=metadata.user_id,
            note=serializer.validated_data.get('note'),
        )
        return ResponseHandler.api_success(shipment)
