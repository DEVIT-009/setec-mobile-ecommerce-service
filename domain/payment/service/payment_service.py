from abc import ABC, abstractmethod
from typing import Any, Dict


class PaymentServiceInterface(ABC):
    @abstractmethod
    def complete(self, order_id: str, user_id: str, idempotency_key: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_for_order(self, order_id: str, user_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def complete_batch(
        self,
        order_ids: list[str],
        user_id: str,
        idempotency_key: str,
    ) -> Dict[str, Any]:
        pass
