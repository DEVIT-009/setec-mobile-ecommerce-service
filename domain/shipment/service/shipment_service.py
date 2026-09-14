from abc import ABC, abstractmethod
from typing import List, Dict, Any

class ShipmentServiceInterface(ABC):
    @abstractmethod
    def list_by_order(self, order_id: str, user_id: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_detail(self, shipment_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_events(self, shipment_id: str) -> List[Dict[str, Any]]:
        pass
