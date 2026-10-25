from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple
from domain.shipment.entity.shipment import Shipment, ShipmentEvent

class ShipmentRepositoryInterface(ABC):
    @abstractmethod
    def list_by_order(self, order_id: str, user_id: str) -> List[Shipment]: pass
    @abstractmethod
    def get_by_id(self, shipment_id: str, user_id: Optional[str] = None) -> Optional[Shipment]: pass
    @abstractmethod
    def get_events(self, shipment_id: str, user_id: Optional[str] = None) -> List[ShipmentEvent]: pass
    @abstractmethod
    def create_for_order(self, order_id: str, actor_id: str, note: Optional[str] = None) -> Shipment: pass
    @abstractmethod
    def mark_packed(self, shipment_id: str, actor_id: str, note: Optional[str] = None) -> Shipment: pass
    @abstractmethod
    def handoff(self, shipment_id: str, actor_id: str, data: Dict[str, Any]) -> Shipment: pass
    @abstractmethod
    def list_admin(self, page: int, page_size: int) -> Tuple[List[Shipment], int]: pass
    @abstractmethod
    def update_tracking(self, shipment_id: str, actor_id: str, data: Dict[str, Any]) -> Shipment: pass
    @abstractmethod
    def record_checkpoint(self, shipment_id: str, actor_id: str, data: Dict[str, Any]) -> ShipmentEvent: pass
    @abstractmethod
    def mark_out_for_delivery(self, shipment_id: str, actor_id: str, data: Dict[str, Any]) -> Shipment: pass
    @abstractmethod
    def confirm_delivery(self, shipment_id: str, user_id: str, note: Optional[str] = None) -> Shipment: pass
