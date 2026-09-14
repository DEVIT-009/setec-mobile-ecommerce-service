from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

@dataclass
class ShipmentEvent:
    id: Optional[str] = None
    shipment_id: Optional[str] = None
    status: str = ""
    location: Optional[str] = None
    description: Optional[str] = None
    event_time: Optional[datetime] = None
    created_at: Optional[datetime] = None

@dataclass
class Shipment:
    id: Optional[str] = None
    order_id: Optional[str] = None
    carrier_name: Optional[str] = None
    tracking_number: Optional[str] = None
    status: str = "pending"
    shipped_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    events: List[ShipmentEvent] = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
