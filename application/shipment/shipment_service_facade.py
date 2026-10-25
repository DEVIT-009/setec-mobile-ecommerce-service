from typing import List, Dict, Any, Optional
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

    def get_detail(self, shipment_id: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        shipment = self.repo.get_by_id(shipment_id, user_id)
        if not shipment:
            raise ShipmentException.not_found()
        events = self.repo.get_events(shipment_id, user_id)
        shipment.events = events
        return ShipmentControllerMapper.to_response(shipment, with_events=True)

    def get_events(self, shipment_id: str, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        events = self.repo.get_events(shipment_id, user_id)
        return [ShipmentControllerMapper.event_to_response(e) for e in events]

    def create_for_order(self, order_id: str, actor_id: str, note: Optional[str] = None) -> Dict[str, Any]:
        shipment = self.repo.create_for_order(order_id, actor_id, note)
        return ShipmentControllerMapper.to_response(shipment, with_events=True)

    def mark_packed(self, shipment_id: str, actor_id: str, note: Optional[str] = None) -> Dict[str, Any]:
        shipment = self.repo.mark_packed(shipment_id, actor_id, note)
        return ShipmentControllerMapper.to_response(shipment, with_events=True)

    def handoff(self, shipment_id: str, actor_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        shipment = self.repo.handoff(shipment_id, actor_id, data)
        return ShipmentControllerMapper.to_response(shipment, with_events=True)

    def list_admin(self, page: int, page_size: int) -> Dict[str, Any]:
        shipments, total = self.repo.list_admin(page, page_size)
        return {
            "items": ShipmentControllerMapper.to_list_response(shipments),
            "total": total,
        }

    def update_tracking(self, shipment_id: str, actor_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        shipment = self.repo.update_tracking(shipment_id, actor_id, data)
        return ShipmentControllerMapper.to_response(shipment, with_events=True)

    def record_checkpoint(self, shipment_id: str, actor_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        event = self.repo.record_checkpoint(shipment_id, actor_id, data)
        return ShipmentControllerMapper.event_to_response(event)

    def mark_out_for_delivery(self, shipment_id: str, actor_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        shipment = self.repo.mark_out_for_delivery(shipment_id, actor_id, data)
        return ShipmentControllerMapper.to_response(shipment, with_events=True)

    def confirm_delivery(self, shipment_id: str, user_id: str, note: Optional[str] = None) -> Dict[str, Any]:
        shipment = self.repo.confirm_delivery(shipment_id, user_id, note)
        return ShipmentControllerMapper.to_response(shipment, with_events=True)
