from decimal import Decimal
from collections import defaultdict
from typing import Optional, List, Tuple, Dict, Any
from django.utils import timezone
from django.db import transaction

from domain.order.ports.order_repository import OrderRepositoryInterface
from domain.order.entity.order import Order
from domain.order.exception.order_exception import OrderException
from infrastructure.persistence.mapper.order_persistence_mapper import OrderPersistenceMapper
from infrastructure.persistence.models.order_model import (
    Order as OrderModel,
    OrderItem as OrderItemModel,
    OrderStatusHistory as OrderStatusHistoryModel,
)
from infrastructure.persistence.models.cart_model import Cart as CartModel, CartItem as CartItemModel


class OrderRepositoryInterfaceImpl(OrderRepositoryInterface):

    CANCELLABLE_STATUSES = {'pending', 'confirmed'}

    @transaction.atomic
    def place_orders(self, cart_id: str, shipping_address_id: str, user_id: str, idempotency_key: Optional[str] = None) -> List[Order]:
        cart = CartModel.objects.filter(id=cart_id, user_id=user_id, status='active', deleted_at__isnull=True).first()
        if not cart:
            raise OrderException.empty_cart()

        selected_items = CartItemModel.objects.filter(
            cart=cart, is_selected=True, deleted_at__isnull=True
        ).select_related('product__store', 'product_variant')

        if not selected_items.exists():
            raise OrderException.empty_cart()

        store_groups = defaultdict(list)
        for item in selected_items:
            store_groups[item.product.store_id].append(item)

        created_orders = []
        for store_id, items in store_groups.items():
            subtotal = sum(i.unit_price_snapshot * i.quantity for i in items)

            # ID is auto-generated via model.save() using generate_order_id()
            order_model = OrderModel.objects.create(
                user_id=user_id,
                store_id=store_id,
                shipping_address_id=shipping_address_id,
                status='pending',
                subtotal_amount=subtotal,
                shipping_amount=Decimal("0.00"),
                discount_amount=Decimal("0.00"),
                tax_amount=Decimal("0.00"),
                total_amount=subtotal,
                currency='USD',
                placed_at=timezone.now(),
            )

            for item in items:
                OrderItemModel.objects.create(
                    order=order_model,
                    product_id=item.product_id,
                    product_variant_id=item.product_variant_id,
                    product_name_snapshot=item.product.name,
                    variant_name_snapshot=item.product_variant.name if item.product_variant else None,
                    sku_snapshot=item.product_variant.sku if item.product_variant and item.product_variant.sku else item.product.sku,
                    unit_price=item.unit_price_snapshot,
                    quantity=item.quantity,
                    line_total=item.unit_price_snapshot * item.quantity,
                )

            OrderStatusHistoryModel.objects.create(
                order=order_model,
                from_status=None,
                to_status='pending',
                changed_by_id=user_id,
                note='Order placed via cart checkout',
            )

            created_orders.append(OrderPersistenceMapper.from_entity(order_model))

        # Mark cart checked out & soft-delete processed items
        cart.status = 'checked_out'
        cart.save()
        selected_items.update(deleted_at=timezone.now())

        return created_orders

    def list_by_user(self, user_id: str, page: int, page_size: int) -> Tuple[List[Order], int]:
        qs = OrderModel.objects.filter(user_id=user_id, deleted_at__isnull=True).order_by('-created_at').select_related('store')
        total = qs.count()
        offset = (page - 1) * page_size
        models = list(qs[offset:offset + page_size])
        return [OrderPersistenceMapper.from_entity(m) for m in models if m is not None], total

    def get_by_id(self, order_id: str, user_id: Optional[str] = None) -> Optional[Order]:
        qs = OrderModel.objects.filter(id=order_id, deleted_at__isnull=True).select_related('store')
        if user_id:
            qs = qs.filter(user_id=user_id)
        model = qs.first()
        if not model:
            return None
        return OrderPersistenceMapper.from_entity(model)

    @transaction.atomic
    def cancel(self, order_id: str, user_id: str) -> Order:
        order = OrderModel.objects.filter(id=order_id, user_id=user_id, deleted_at__isnull=True).first()
        if not order:
            raise OrderException.not_found()
        if order.status not in self.CANCELLABLE_STATUSES:
            raise OrderException.cannot_cancel()

        old_status = order.status
        order.status = 'cancelled'
        order.cancelled_at = timezone.now()
        order.save()

        OrderStatusHistoryModel.objects.create(
            order=order,
            from_status=old_status,
            to_status='cancelled',
            changed_by_id=user_id,
            note='Cancelled by customer',
        )
        return OrderPersistenceMapper.from_entity(order)

    def get_status_history(self, order_id: str) -> List[Dict[str, Any]]:
        history = OrderStatusHistoryModel.objects.filter(order_id=order_id).order_by('created_at')
        return [
            {
                "id": str(h.id),
                "from_status": h.from_status,
                "to_status": h.to_status,
                "note": h.note,
                "created_at": h.created_at.isoformat() if h.created_at else None,
            }
            for h in history
        ]

    def list_admin(self, filters: dict, page: int, page_size: int) -> Tuple[List[Order], int]:
        qs = OrderModel.objects.filter(deleted_at__isnull=True).order_by('-created_at').select_related('store', 'user')
        if filters.get('status'):
            qs = qs.filter(status=filters['status'])
        if filters.get('user_id'):
            qs = qs.filter(user_id=filters['user_id'])
        if filters.get('store_id'):
            qs = qs.filter(store_id=filters['store_id'])

        total = qs.count()
        offset = (page - 1) * page_size
        models = list(qs[offset:offset + page_size])
        return [OrderPersistenceMapper.from_entity(m) for m in models if m is not None], total

    @transaction.atomic
    def update_status(self, order_id: str, status: str, changed_by_user_id: str, note: Optional[str] = None) -> Order:
        order = OrderModel.objects.filter(id=order_id, deleted_at__isnull=True).first()
        if not order:
            raise OrderException.not_found()

        old_status = order.status
        order.status = status
        order.save()

        OrderStatusHistoryModel.objects.create(
            order=order,
            from_status=old_status,
            to_status=status,
            changed_by_id=changed_by_user_id,
            note=note,
        )
        return OrderPersistenceMapper.from_entity(order)
