from typing import Optional, List
from domain.shipment.entity.shipment import Shipment as DomainShipment, ShipmentEvent as DomainShipmentEvent
from infrastructure.persistence.models.shipment_model import (
    Shipment as ShipmentModel,
    ShipmentEvent as ShipmentEventModel,
)


class ShipmentPersistenceMapper:

    @staticmethod
    def event_from_entity(entity: Optional[ShipmentEventModel]) -> Optional[DomainShipmentEvent]:
        if entity is None:
            return None
        return DomainShipmentEvent(
            id=str(entity.id),
            shipment_id=str(entity.shipment_id) if entity.shipment_id else None,
            status=entity.status,
            location=entity.location,
            description=entity.description,
            event_time=entity.event_time,
            created_at=entity.created_at,
        )

    @staticmethod
    def from_entity(entity: Optional[ShipmentModel]) -> Optional[DomainShipment]:
        if entity is None:
            return None
        
        events = []
        if hasattr(entity, 'events'):
            events = [ShipmentPersistenceMapper.event_from_entity(e) for e in entity.events.all() if e is not None]

        return DomainShipment(
            id=str(entity.id),
            order_id=str(entity.order_id) if entity.order_id else None,
            carrier_name=entity.carrier_name,
            tracking_number=entity.tracking_number,
            status=entity.status,
            shipped_at=entity.shipped_at,
            delivered_at=entity.delivered_at,
            events=events,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
