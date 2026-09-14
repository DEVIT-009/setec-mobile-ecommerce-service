from rest_framework.views import APIView
from rest_framework.request import Request

from application.cart.factory.cart_service_factory import cart_service_factory
from interface.cart.serializer.request.cart_request import (
    CartItemRequest,
    CartItemUpdateRequest,
    SelectAllRequest,
    CheckoutPreviewRequest,
    CartItemSerializer,
    CartItemUpdateSerializer,
    SelectAllSerializer,
    CheckoutPreviewSerializer,
)
from shared.responseutils.response_handler import ResponseHandler
from shared.metadata_handler.request_header_utillity import metadata_handler


class CartView(APIView):
    @metadata_handler(required_user_id=True)
    def get(self, request: Request, metadata=None):
        service = cart_service_factory()
        return ResponseHandler.api_success(service.get_or_create_cart(metadata.user_id))


class CartItemListView(APIView):
    @metadata_handler(required_user_id=True)
    def post(self, request: Request, metadata=None):
        serializer = CartItemRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = cart_service_factory()
        return ResponseHandler.api_created(service.add_item(metadata.user_id, {
            'product_id': str(serializer.validated_data['product_id']),
            'product_variant_id': str(serializer.validated_data['product_variant_id']) if serializer.validated_data.get('product_variant_id') else None,
            'quantity': serializer.validated_data['quantity'],
        }))


class CartItemDetailView(APIView):
    @metadata_handler(required_user_id=True)
    def patch(self, request: Request, cart_item_id=None, metadata=None):
        serializer = CartItemUpdateRequest(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        service = cart_service_factory()
        return ResponseHandler.api_success(service.update_item(metadata.user_id, str(cart_item_id), serializer.validated_data))

    @metadata_handler(required_user_id=True)
    def delete(self, request: Request, cart_item_id=None, metadata=None):
        service = cart_service_factory()
        service.delete_item(metadata.user_id, str(cart_item_id))
        return ResponseHandler.api_no_content()


class CartSelectAllView(APIView):
    @metadata_handler(required_user_id=True)
    def post(self, request: Request, metadata=None):
        serializer = SelectAllRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = cart_service_factory()
        return ResponseHandler.api_success(service.select_all(metadata.user_id, serializer.validated_data['selected']))


class CartCheckoutPreviewView(APIView):
    @metadata_handler(required_user_id=True)
    def post(self, request: Request, metadata=None):
        serializer = CheckoutPreviewRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        shipping_address_id = str(serializer.validated_data['shipping_address_id']) if serializer.validated_data.get('shipping_address_id') else None
        service = cart_service_factory()
        return ResponseHandler.api_success(service.checkout_preview(metadata.user_id, shipping_address_id=shipping_address_id))

