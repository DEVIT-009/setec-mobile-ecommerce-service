from abc import ABC, abstractmethod
from typing import Optional, List, Tuple, Dict, Any
from domain.order.entity.order import Order

class OrderRepositoryInterface(ABC):
    @abstractmethod
    def place_orders(self, cart_id: str, shipping_address_id: str, user_id: str, idempotency_key: Optional[str] = None) -> List[Order]: pass
    @abstractmethod
    def list_by_user(self, user_id: str, page: int, page_size: int) -> Tuple[List[Order], int]: pass
    @abstractmethod
    def get_by_id(self, order_id: str, user_id: Optional[str] = None) -> Optional[Order]: pass
    @abstractmethod
    def cancel(self, order_id: str, user_id: str) -> Order: pass
    @abstractmethod
    def get_status_history(self, order_id: str) -> List[Dict[str, Any]]: pass
    @abstractmethod
    def list_admin(self, filters: dict, page: int, page_size: int) -> Tuple[List[Order], int]: pass
    @abstractmethod
    def update_status(self, order_id: str, status: str, changed_by_user_id: str, note: Optional[str] = None) -> Order: pass
