from rest_framework.request import Request
from rest_framework.views import APIView

from application.payment.factory.payment_service_factory import payment_service_factory
from interface.payment.serializer.request.payment_request import (
    CompleteInternalPaymentBatchRequest,
    CompleteInternalPaymentRequest,
)
from shared.metadata_handler.request_header_utillity import metadata_handler
from shared.responseutils.response_handler import ResponseHandler


class OrderPaymentView(APIView):
    @metadata_handler(required_user_id=True)
    def get(self, request: Request, order_id=None, metadata=None):
        service = payment_service_factory()
        payment = service.get_for_order(str(order_id), metadata.user_id)
        return ResponseHandler.api_success(payment)

    @metadata_handler(required_user_id=True)
    def post(self, request: Request, order_id=None, metadata=None):
        serializer = CompleteInternalPaymentRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = payment_service_factory()
        payment = service.complete(
            order_id=str(order_id),
            user_id=metadata.user_id,
            idempotency_key=serializer.validated_data['idempotency_key'],
            outcome=serializer.validated_data['simulate_outcome'],
            failure_reason=serializer.validated_data.get('failure_reason'),
        )
        return ResponseHandler.api_created(payment)


class OrderBatchPaymentView(APIView):
    @metadata_handler(required_user_id=True)
    def post(self, request: Request, metadata=None):
        serializer = CompleteInternalPaymentBatchRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = payment_service_factory()
        batch = service.complete_batch(
            order_ids=[str(order_id) for order_id in serializer.validated_data['order_ids']],
            user_id=metadata.user_id,
            idempotency_key=serializer.validated_data['idempotency_key'],
            outcome=serializer.validated_data['simulate_outcome'],
            failure_reason=serializer.validated_data.get('failure_reason'),
        )
        return ResponseHandler.api_created(batch)
