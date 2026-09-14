from typing import List, Dict, Any
from domain.shipment.ports.shipment_repository import ShipmentRepositoryInterface
from domain.shipment.service.shipment_service import ShipmentServiceInterface
from domain.shipment.exception.shipment_exception import ShipmentException
from interface.shipment.serializer.mapper.shipment_controller_mapper import ShipmentControllerMapper


class ShipmentServiceFacade(ShipmentServiceInterface):

    def __init__(self, repo: ShipmentRepositoryInterface):
        self.repo = repo

    def list_by_order(self, order_id: str, user_id: str) -> List[Dict[str, Any]]:
        shipments = self.repo.list_by_order(order_id, user_id)
        return ShipmentControllerMapper.to_list_response(shipments)

    def get_detail(self, shipment_id: str) -> Dict[str, Any]:
        shipment = self.repo.get_by_id(shipment_id)
        if not shipment:
            raise ShipmentException.not_found()
        events = self.repo.get_events(shipment_id)
        shipment.events = events
        return ShipmentControllerMapper.to_response(shipment, with_events=True)

    def get_events(self, shipment_id: str) -> List[Dict[str, Any]]:
        events = self.repo.get_events(shipment_id)
        return [ShipmentControllerMapper.event_to_response(e) for e in events]
