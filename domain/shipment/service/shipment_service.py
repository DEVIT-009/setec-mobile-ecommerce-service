from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class ShipmentServiceInterface(ABC):
    @abstractmethod
    def list_by_order(self, order_id: str, user_id: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_detail(self, shipment_id: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_events(self, shipment_id: str, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def create_for_order(self, order_id: str, actor_id: str, note: Optional[str] = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    def mark_packed(self, shipment_id: str, actor_id: str, note: Optional[str] = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    def handoff(self, shipment_id: str, actor_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def list_admin(self, page: int, page_size: int) -> Dict[str, Any]:
        pass

    @abstractmethod
    def update_tracking(self, shipment_id: str, actor_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def record_checkpoint(self, shipment_id: str, actor_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def mark_out_for_delivery(self, shipment_id: str, actor_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def confirm_delivery(self, shipment_id: str, user_id: str, note: Optional[str] = None) -> Dict[str, Any]:
        pass
