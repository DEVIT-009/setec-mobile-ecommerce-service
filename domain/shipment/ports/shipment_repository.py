from abc import ABC, abstractmethod
from typing import List, Optional
from domain.shipment.entity.shipment import Shipment, ShipmentEvent

class ShipmentRepositoryInterface(ABC):
    @abstractmethod
    def list_by_order(self, order_id: str, user_id: str) -> List[Shipment]: pass
    @abstractmethod
    def get_by_id(self, shipment_id: str) -> Optional[Shipment]: pass
    @abstractmethod
    def get_events(self, shipment_id: str) -> List[ShipmentEvent]: pass
