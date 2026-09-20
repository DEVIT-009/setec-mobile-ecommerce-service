from rest_framework.views import APIView
from rest_framework.request import Request

from application.order.factory.order_service_factory import order_service_factory
from interface.order.serializer.request.order_request import (
    AdminOrderUpdateStatusRequest,
    AdminOrderUpdateStatusSerializer,
    ORDER_STATUS_CHOICES,
)
from shared.responseutils.response_handler import ResponseHandler
from shared.metadata_handler.request_header_utillity import metadata_handler
from shared.permission_handler import require_roles
from shared.pagination.api_paging import ApiPaging



class AdminOrderListView(APIView):
    """
    GET /api/v1/admin/orders/  — list all non-deleted orders (active + all statuses).
    """

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def get(self, request: Request, metadata=None):
        paging = ApiPaging.from_request(request)
        filters = {
            'user_id': request.query_params.get('user_id'),
            'status': request.query_params.get('status'),
            'store_id': request.query_params.get('store_id'),
        }
        service = order_service_factory()
        result = service.list_admin(filters=filters, page=paging['page'], page_size=paging['page_size'])
        return ResponseHandler.api_list(result['items'], paging['page'], paging['page_size'], result['total'])


class AdminOrderDetailView(APIView):
    """
    GET   /api/v1/admin/orders/<str:order_id>/
    PATCH /api/v1/admin/orders/<str:order_id>/status/  — handled by AdminOrderStatusView
    """

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def get(self, request: Request, order_id=None, metadata=None):
        service = order_service_factory()
        return ResponseHandler.api_success(service.get_detail(str(order_id), user_id=None))


class AdminOrderStatusView(APIView):
    """
    PATCH /api/v1/admin/orders/<str:order_id>/status/
    """

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def patch(self, request: Request, order_id=None, metadata=None):
        serializer = AdminOrderUpdateStatusRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = order_service_factory()
        result = service.update_status(
            str(order_id),
            serializer.validated_data['status'],
            changed_by_user_id=metadata.user_id,
            note=serializer.validated_data.get('note'),
        )
        return ResponseHandler.api_success(result)

