from typing import Dict, Any, List
from dataclasses import asdict
from domain.shipment.entity.shipment import Shipment, ShipmentEvent
from interface.shipment.serializer.response.shipment_response import (
    ShipmentResponse,
    ShipmentEventResponse,
)


class ShipmentControllerMapper:

    @staticmethod
    def event_to_response(event: ShipmentEvent) -> Dict[str, Any]:
        response_dto = ShipmentEventResponse(
            id=str(event.id) if event.id else None,
            status=event.status,
            location=event.location,
            description=event.description,
            event_time=event.event_time.isoformat() if event.event_time else None,
        )
        return asdict(response_dto)

    @staticmethod
    def to_response(shipment: Shipment, with_events: bool = False) -> Dict[str, Any]:
        events = [ShipmentControllerMapper.event_to_response(e) for e in shipment.events] if with_events else None
        response_dto = ShipmentResponse(
            id=str(shipment.id) if shipment.id else None,
            order_id=str(shipment.order_id) if shipment.order_id else None,
            carrier_name=shipment.carrier_name,
            tracking_number=shipment.tracking_number,
            status=shipment.status,
            shipped_at=shipment.shipped_at.isoformat() if shipment.shipped_at else None,
            delivered_at=shipment.delivered_at.isoformat() if shipment.delivered_at else None,
            events=events,
        )
        data = asdict(response_dto)
        if not with_events:
            data.pop("events", None)
        return data

    @staticmethod
    def to_list_response(shipments: List[Shipment]) -> List[Dict[str, Any]]:
        return [ShipmentControllerMapper.to_response(s) for s in shipments]

