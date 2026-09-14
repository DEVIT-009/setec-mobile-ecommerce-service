from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class OrderServiceInterface(ABC):
    @abstractmethod
    def place_orders(self, user_id: str, cart_id: str, shipping_address_id: str, idempotency_key: Optional[str] = None) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def list(self, user_id: str, page: int, page_size: int) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_detail(self, order_id: str, user_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def cancel(self, order_id: str, user_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_status_history(self, order_id: str, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def list_admin(self, filters: dict, page: int, page_size: int) -> Dict[str, Any]:
        pass

    @abstractmethod
    def update_status(self, order_id: str, status: str, changed_by_user_id: str, note: Optional[str] = None) -> Dict[str, Any]:
        pass
