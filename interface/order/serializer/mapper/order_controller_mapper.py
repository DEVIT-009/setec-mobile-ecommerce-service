from typing import Dict, Any, List
from dataclasses import asdict
from domain.order.entity.order import Order, OrderItem, OrderStatusEntry
from interface.order.serializer.response.order_response import (
    OrderItemResponse,
    OrderSummaryResponse,
    OrderDetailResponse,
)


class OrderControllerMapper:

    @staticmethod
    def item_to_response(item: OrderItem) -> Dict[str, Any]:
        response_dto = OrderItemResponse(
            id=str(item.id) if item.id else None,
            product_id=str(item.product_id) if item.product_id else None,
            product_variant_id=str(item.product_variant_id) if item.product_variant_id else None,
            product_name=item.product_name_snapshot,
            variant_name=item.variant_name_snapshot,
            sku=item.sku_snapshot,
            unit_price=str(item.unit_price),
            quantity=item.quantity,
            line_total=str(item.line_total),
        )
        return asdict(response_dto)

    @staticmethod
    def to_summary_response(order: Order) -> Dict[str, Any]:
        response_dto = OrderSummaryResponse(
            id=str(order.id) if order.id else None,
            order_number=order.order_number,
            status=order.status,
            total_amount=str(order.total_amount),
            currency=order.currency,
            store={"id": order.store_id, "name": order.store_name} if order.store_id else None,
            item_count=len(order.items),
            placed_at=order.placed_at.isoformat() if order.placed_at else (order.created_at.isoformat() if order.created_at else None),
        )
        return asdict(response_dto)

    @staticmethod
    def to_detail_response(order: Order, shipment_summary: Any = None) -> Dict[str, Any]:
        response_dto = OrderDetailResponse(
            id=str(order.id) if order.id else None,
            order_number=order.order_number,
            status=order.status,
            subtotal_amount=str(order.subtotal_amount),
            shipping_amount=str(order.shipping_amount),
            discount_amount=str(order.discount_amount),
            tax_amount=str(order.tax_amount),
            total_amount=str(order.total_amount),
            currency=order.currency,
            placed_at=order.placed_at.isoformat() if order.placed_at else (order.created_at.isoformat() if order.created_at else None),
            cancelled_at=order.cancelled_at.isoformat() if order.cancelled_at else None,
            store={"id": order.store_id, "name": order.store_name} if order.store_id else None,
            shipping_address_id=str(order.shipping_address_id) if order.shipping_address_id else None,
            items=[OrderControllerMapper.item_to_response(i) for i in order.items],
            payment=None,
            shipments=shipment_summary or [],
            status_history=[
                {
                    "id": str(h.id) if h.id else None,
                    "from_status": h.from_status,
                    "to_status": h.to_status,
                    "note": h.note,
                    "created_at": h.created_at.isoformat() if h.created_at else None,
                }
                for h in order.status_history
            ],
        )
        return asdict(response_dto)

    @staticmethod
    def to_summary_list_response(orders: List[Order]) -> List[Dict[str, Any]]:
        return [OrderControllerMapper.to_summary_response(o) for o in orders]

