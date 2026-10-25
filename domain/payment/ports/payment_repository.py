from abc import ABC, abstractmethod
from typing import Optional

from domain.payment.entity.payment import Payment, PaymentBatch


class PaymentRepositoryInterface(ABC):
    @abstractmethod
    def complete_internal_payment(
        self,
        order_id: str,
        user_id: str,
        idempotency_key: str,
    ) -> Payment:
        pass

    @abstractmethod
    def get_by_order(self, order_id: str, user_id: str) -> Optional[Payment]:
        pass

    @abstractmethod
    def complete_internal_batch(
        self,
        order_ids: list[str],
        user_id: str,
        idempotency_key: str,
    ) -> PaymentBatch:
        pass
