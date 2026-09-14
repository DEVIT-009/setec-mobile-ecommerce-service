from decimal import Decimal
from typing import Optional, List
from domain.order.entity.order import Order as DomainOrder, OrderItem as DomainOrderItem, OrderStatusEntry as DomainOrderStatusEntry
from infrastructure.persistence.models.order_model import (
    Order as OrderModel,
    OrderItem as OrderItemModel,
    OrderStatusHistory as OrderStatusHistoryModel,
)


class OrderPersistenceMapper:

    @staticmethod
    def item_from_entity(entity: Optional[OrderItemModel]) -> Optional[DomainOrderItem]:
        if entity is None:
            return None
        return DomainOrderItem(
            id=str(entity.id),
            order_id=str(entity.order_id) if entity.order_id else None,
            product_id=str(entity.product_id) if entity.product_id else None,
            product_variant_id=str(entity.product_variant_id) if entity.product_variant_id else None,
            product_name_snapshot=entity.product_name_snapshot,
            variant_name_snapshot=entity.variant_name_snapshot,
            sku_snapshot=entity.sku_snapshot,
            unit_price=Decimal(str(entity.unit_price)),
            quantity=entity.quantity,
            line_total=Decimal(str(entity.line_total)),
        )

    @staticmethod
    def status_entry_from_entity(entity: Optional[OrderStatusHistoryModel]) -> Optional[DomainOrderStatusEntry]:
        if entity is None:
            return None
        return DomainOrderStatusEntry(
            id=str(entity.id),
            order_id=str(entity.order_id) if entity.order_id else None,
            from_status=entity.from_status,
            to_status=entity.to_status,
            note=entity.note,
            created_at=entity.created_at,
        )

    @staticmethod
    def from_entity(entity: Optional[OrderModel]) -> Optional[DomainOrder]:
        if entity is None:
            return None
        
        items = []
        if hasattr(entity, 'items'):
            items = [OrderPersistenceMapper.item_from_entity(i) for i in entity.items.all() if i is not None]

        status_history = []
        if hasattr(entity, 'status_history'):
            status_history = [OrderPersistenceMapper.status_entry_from_entity(sh) for sh in entity.status_history.all() if sh is not None]

        return DomainOrder(
            id=str(entity.id),
            order_number=entity.order_number,
            user_id=str(entity.user_id) if entity.user_id else None,
            store_id=str(entity.store_id) if entity.store_id else None,
            store_name=entity.store.name if getattr(entity, 'store', None) else None,
            shipping_address_id=str(entity.shipping_address_id) if entity.shipping_address_id else None,
            status=entity.status,
            subtotal_amount=Decimal(str(entity.subtotal_amount)),
            shipping_amount=Decimal(str(entity.shipping_amount)),
            discount_amount=Decimal(str(entity.discount_amount)),
            tax_amount=Decimal(str(entity.tax_amount)),
            total_amount=Decimal(str(entity.total_amount)),
            currency=entity.currency,
            placed_at=entity.placed_at,
            cancelled_at=entity.cancelled_at,
            items=items,
            status_history=status_history,
            payment=None,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )
