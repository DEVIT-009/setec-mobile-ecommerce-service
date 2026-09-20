from rest_framework.views import APIView
from rest_framework.request import Request

from application.shipment.factory.shipment_service_factory import shipment_service_factory
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
        service = shipment_service_factory()
        return ResponseHandler.api_success(service.update(str(shipment_id), request.data, actor_id=metadata.user_id))
