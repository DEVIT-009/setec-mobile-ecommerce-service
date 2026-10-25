from typing import Any, Dict

from domain.payment.exception.payment_exception import PaymentException
from domain.payment.ports.payment_repository import PaymentRepositoryInterface
from domain.payment.service.payment_service import PaymentServiceInterface
from interface.payment.serializer.mapper.payment_controller_mapper import PaymentControllerMapper


class PaymentServiceFacade(PaymentServiceInterface):
    def __init__(self, repo: PaymentRepositoryInterface):
        self.repo = repo

    def complete(self, order_id: str, user_id: str, idempotency_key: str) -> Dict[str, Any]:
        payment = self.repo.complete_internal_payment(order_id, user_id, idempotency_key)
        return PaymentControllerMapper.to_response(payment)

    def get_for_order(self, order_id: str, user_id: str) -> Dict[str, Any]:
        payment = self.repo.get_by_order(order_id, user_id)
        if not payment:
            raise PaymentException.not_found()
        return PaymentControllerMapper.to_response(payment)

    def complete_batch(
        self,
        order_ids: list[str],
        user_id: str,
        idempotency_key: str,
    ) -> Dict[str, Any]:
        batch = self.repo.complete_internal_batch(order_ids, user_id, idempotency_key)
        return PaymentControllerMapper.to_batch_response(batch)
