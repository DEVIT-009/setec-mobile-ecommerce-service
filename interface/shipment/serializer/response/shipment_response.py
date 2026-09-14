from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class ShipmentEventResponse:
    id: Optional[str]
    status: str
    location: Optional[str] = None
    description: Optional[str] = None
    event_time: Optional[str] = None

    def to_dict(self):
        return self.__dict__


@dataclass
class ShipmentResponse:
    id: Optional[str]
    order_id: Optional[str]
    carrier_name: str
    tracking_number: str
    status: str
    shipped_at: Optional[str] = None
    delivered_at: Optional[str] = None
    events: Optional[List[Dict[str, Any]]] = None

    def to_dict(self):
        return self.__dict__
