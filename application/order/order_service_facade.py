from typing import Optional, List, Dict, Any
from domain.order.ports.order_repository import OrderRepositoryInterface
from domain.order.service.order_service import OrderServiceInterface
from domain.order.exception.order_exception import OrderException
from interface.order.serializer.mapper.order_controller_mapper import OrderControllerMapper


class OrderServiceFacade(OrderServiceInterface):

    def __init__(self, repo: OrderRepositoryInterface):
        self.repo = repo

    def place_orders(self, user_id: str, cart_id: str, shipping_address_id: str, idempotency_key: Optional[str] = None) -> List[Dict[str, Any]]:
        orders = self.repo.place_orders(
            cart_id=cart_id,
            shipping_address_id=shipping_address_id,
            user_id=user_id,
            idempotency_key=idempotency_key,
        )
        return [OrderControllerMapper.to_detail_response(o) for o in orders]

    def list(self, user_id: str, page: int, page_size: int) -> Dict[str, Any]:
        orders, total = self.repo.list_by_user(user_id, page, page_size)
        return {
            "items": OrderControllerMapper.to_summary_list_response(orders),
            "total": total,
        }

    def get_detail(self, order_id: str, user_id: str) -> Dict[str, Any]:
        order = self.repo.get_by_id(order_id, user_id)
        if not order:
            raise OrderException.not_found()
        return OrderControllerMapper.to_detail_response(order)

    def cancel(self, order_id: str, user_id: str) -> Dict[str, Any]:
        order = self.repo.cancel(order_id, user_id)
        return OrderControllerMapper.to_detail_response(order)

    def get_status_history(self, order_id: str, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        return self.repo.get_status_history(order_id)

    def list_admin(self, filters: dict, page: int, page_size: int) -> Dict[str, Any]:
        orders, total = self.repo.list_admin(filters, page, page_size)
        return {
            "items": [OrderControllerMapper.to_detail_response(o) for o in orders],
            "total": total,
        }

    def update_status(self, order_id: str, status: str, changed_by_user_id: str, note: Optional[str] = None) -> Dict[str, Any]:
        order = self.repo.update_status(order_id, status, changed_by_user_id, note)
        return OrderControllerMapper.to_detail_response(order)
