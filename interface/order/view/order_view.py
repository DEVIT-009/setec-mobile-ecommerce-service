from rest_framework.views import APIView
from rest_framework.request import Request

from application.order.factory.order_service_factory import order_service_factory
from application.shipment.factory.shipment_service_factory import shipment_service_factory
from interface.order.serializer.request.order_request import PlaceOrderRequest, PlaceOrderSerializer
from shared.responseutils.response_handler import ResponseHandler
from shared.metadata_handler.request_header_utillity import metadata_handler
from shared.pagination.api_paging import ApiPaging


class OrderListView(APIView):
    @metadata_handler(required_user_id=True)
    def get(self, request: Request, metadata=None):
        paging = ApiPaging.from_request(request)
        service = order_service_factory()
        result = service.list(metadata.user_id, page=paging['page'], page_size=paging['page_size'])
        return ResponseHandler.api_list(result['items'], paging['page'], paging['page_size'], result['total'])

    @metadata_handler(required_user_id=True)
    def post(self, request: Request, metadata=None):
        serializer = PlaceOrderRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = order_service_factory()
        orders = service.place_orders(
            user_id=metadata.user_id,
            cart_id=str(serializer.validated_data['cart_id']),
            shipping_address_id=str(serializer.validated_data['shipping_address_id']),
            idempotency_key=serializer.validated_data['idempotency_key'],
        )
        return ResponseHandler.api_created(orders)



class OrderDetailView(APIView):
    @metadata_handler(required_user_id=True)
    def get(self, request: Request, order_id=None, metadata=None):
        service = order_service_factory()
        return ResponseHandler.api_success(service.get_detail(str(order_id), metadata.user_id))


class OrderCancelView(APIView):
    @metadata_handler(required_user_id=True)
    def post(self, request: Request, order_id=None, metadata=None):
        service = order_service_factory()
        return ResponseHandler.api_success(service.cancel(str(order_id), metadata.user_id))


class OrderStatusHistoryView(APIView):
    @metadata_handler(required_user_id=True)
    def get(self, request: Request, order_id=None, metadata=None):
        service = order_service_factory()
        return ResponseHandler.api_success(service.get_status_history(str(order_id), metadata.user_id))


class OrderShipmentsView(APIView):
    @metadata_handler(required_user_id=True)
    def get(self, request: Request, order_id=None, metadata=None):
        service = shipment_service_factory()
        return ResponseHandler.api_success(service.list_by_order(str(order_id), metadata.user_id))
