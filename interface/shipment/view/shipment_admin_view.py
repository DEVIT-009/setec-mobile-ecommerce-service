from rest_framework.views import APIView
from rest_framework.request import Request

from application.shipment.factory.shipment_service_factory import shipment_service_factory
from interface.shipment.serializer.request.shipment_request import (
    CreateShipmentRequest,
    HandoffShipmentRequest,
    OutForDeliveryRequest,
    PackShipmentRequest,
    ShipmentCheckpointRequest,
    UpdateShipmentTrackingRequest,
)
from shared.responseutils.response_handler import ResponseHandler
from shared.metadata_handler.request_header_utillity import metadata_handler
from shared.permission_handler import require_roles
from shared.pagination.api_paging import ApiPaging


class AdminShipmentListView(APIView):
    """
    GET /api/v1/admin/shipments/  — list all non-deleted shipments.
    """

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def get(self, request: Request, metadata=None):
        paging = ApiPaging.from_request(request)
        service = shipment_service_factory()
        result = service.list_admin(page=paging['page'], page_size=paging['page_size'])
        return ResponseHandler.api_list(result['items'], paging['page'], paging['page_size'], result['total'])


class AdminShipmentDetailView(APIView):
    """
    GET   /api/v1/admin/shipments/<str:shipment_id>/
    PATCH /api/v1/admin/shipments/<str:shipment_id>/  — update tracking/status
    """

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def get(self, request: Request, shipment_id=None, metadata=None):
        service = shipment_service_factory()
        return ResponseHandler.api_success(service.get_detail(str(shipment_id)))

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def patch(self, request: Request, shipment_id=None, metadata=None):
        serializer = UpdateShipmentTrackingRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = shipment_service_factory()
        return ResponseHandler.api_success(service.update_tracking(
            str(shipment_id),
            actor_id=metadata.user_id,
            data=serializer.validated_data,
        ))


class AdminOrderShipmentCreateView(APIView):
    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def post(self, request: Request, order_id=None, metadata=None):
        serializer = CreateShipmentRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = shipment_service_factory()
        shipment = service.create_for_order(
            order_id=str(order_id),
            actor_id=metadata.user_id,
            note=serializer.validated_data.get('note'),
        )
        return ResponseHandler.api_created(shipment)


class AdminShipmentPackedView(APIView):
    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def patch(self, request: Request, shipment_id=None, metadata=None):
        serializer = PackShipmentRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = shipment_service_factory()
        shipment = service.mark_packed(
            shipment_id=str(shipment_id),
            actor_id=metadata.user_id,
            note=serializer.validated_data.get('note'),
        )
        return ResponseHandler.api_success(shipment)


class AdminShipmentHandoffView(APIView):
    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def patch(self, request: Request, shipment_id=None, metadata=None):
        serializer = HandoffShipmentRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = shipment_service_factory()
        shipment = service.handoff(
            shipment_id=str(shipment_id),
            actor_id=metadata.user_id,
            data=serializer.validated_data,
        )
        return ResponseHandler.api_success(shipment)


class AdminShipmentCheckpointView(APIView):
    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def post(self, request: Request, shipment_id=None, metadata=None):
        serializer = ShipmentCheckpointRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = shipment_service_factory()
        event = service.record_checkpoint(
            shipment_id=str(shipment_id),
            actor_id=metadata.user_id,
            data=serializer.validated_data,
        )
        return ResponseHandler.api_created(event)


class AdminShipmentOutForDeliveryView(APIView):
    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def patch(self, request: Request, shipment_id=None, metadata=None):
        serializer = OutForDeliveryRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = shipment_service_factory()
        shipment = service.mark_out_for_delivery(
            shipment_id=str(shipment_id),
            actor_id=metadata.user_id,
            data=serializer.validated_data,
        )
        return ResponseHandler.api_success(shipment)
