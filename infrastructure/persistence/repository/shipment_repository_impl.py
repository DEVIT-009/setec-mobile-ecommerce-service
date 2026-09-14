from typing import List, Optional
from domain.shipment.ports.shipment_repository import ShipmentRepositoryInterface
from domain.shipment.entity.shipment import Shipment, ShipmentEvent
from domain.order.exception.order_exception import OrderException
from domain.shipment.exception.shipment_exception import ShipmentException
from infrastructure.persistence.mapper.shipment_persistence_mapper import ShipmentPersistenceMapper
from infrastructure.persistence.models.shipment_model import (
    Shipment as ShipmentModel,
    ShipmentEvent as ShipmentEventModel,
)
from infrastructure.persistence.models.order_model import Order as OrderModel


class ShipmentRepositoryInterfaceImpl(ShipmentRepositoryInterface):

    def list_by_order(self, order_id: str, user_id: str) -> List[Shipment]:
        order_exists = OrderModel.objects.filter(id=order_id, user_id=user_id, deleted_at__isnull=True).exists()
        if not order_exists:
            raise OrderException.not_found()

        shipments = ShipmentModel.objects.filter(order_id=order_id, deleted_at__isnull=True).order_by('-created_at')
        return [ShipmentPersistenceMapper.from_entity(s) for s in shipments if s is not None]

    def get_by_id(self, shipment_id: str) -> Optional[Shipment]:
        shipment = ShipmentModel.objects.filter(id=shipment_id, deleted_at__isnull=True).first()
        if not shipment:
            return None
        return ShipmentPersistenceMapper.from_entity(shipment)

    def get_events(self, shipment_id: str) -> List[ShipmentEvent]:
        shipment_exists = ShipmentModel.objects.filter(id=shipment_id, deleted_at__isnull=True).exists()
        if not shipment_exists:
            raise ShipmentException.not_found()

        events = ShipmentEventModel.objects.filter(shipment_id=shipment_id).order_by('event_time')
        return [ShipmentPersistenceMapper.event_from_entity(e) for e in events if e is not None]
