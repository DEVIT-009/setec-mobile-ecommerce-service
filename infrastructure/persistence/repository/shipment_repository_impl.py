from typing import Any, Dict, List, Optional, Tuple
from django.db import transaction
from django.utils import timezone
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
from infrastructure.persistence.models.order_status_history_model import OrderStatusHistory


class ShipmentRepositoryInterfaceImpl(ShipmentRepositoryInterface):

    def list_by_order(self, order_id: str, user_id: str) -> List[Shipment]:
        order_exists = OrderModel.objects.filter(id=order_id, user_id=user_id, deleted_at__isnull=True).exists()
        if not order_exists:
            raise OrderException.not_found()

        shipments = ShipmentModel.objects.filter(order_id=order_id, deleted_at__isnull=True).order_by('-created_at')
        return [ShipmentPersistenceMapper.from_entity(s) for s in shipments if s is not None]

    def get_by_id(self, shipment_id: str, user_id: Optional[str] = None) -> Optional[Shipment]:
        qs = ShipmentModel.objects.filter(id=shipment_id, deleted_at__isnull=True)
        if user_id:
            qs = qs.filter(order__user_id=user_id)
        shipment = qs.first()
        if not shipment:
            return None
        return ShipmentPersistenceMapper.from_entity(shipment)

    def get_events(self, shipment_id: str, user_id: Optional[str] = None) -> List[ShipmentEvent]:
        shipment_qs = ShipmentModel.objects.filter(id=shipment_id, deleted_at__isnull=True)
        if user_id:
            shipment_qs = shipment_qs.filter(order__user_id=user_id)
        shipment_exists = shipment_qs.exists()
        if not shipment_exists:
            raise ShipmentException.not_found()

        events = ShipmentEventModel.objects.filter(shipment_id=shipment_id).order_by('event_time')
        return [ShipmentPersistenceMapper.event_from_entity(e) for e in events if e is not None]

    @transaction.atomic
    def create_for_order(self, order_id: str, actor_id: str, note: Optional[str] = None) -> Shipment:
        order = OrderModel.objects.select_for_update().filter(
            id=order_id,
            deleted_at__isnull=True,
        ).first()
        if not order:
            raise OrderException.not_found()

        existing = ShipmentModel.objects.filter(
            order=order,
            deleted_at__isnull=True,
        ).first()
        if existing:
            return ShipmentPersistenceMapper.from_entity(existing)

        if order.status != 'processing':
            raise ShipmentException.order_not_ready(order.status, 'processing')

        now = timezone.now()
        shipment = ShipmentModel.objects.create(
            order=order,
            status='pending',
            created_by_id=actor_id,
            updated_by_id=actor_id,
        )
        ShipmentEventModel.objects.create(
            shipment=shipment,
            status='pending',
            description=note or 'Shipment created',
            event_time=now,
        )
        return ShipmentPersistenceMapper.from_entity(shipment)

    @transaction.atomic
    def mark_packed(self, shipment_id: str, actor_id: str, note: Optional[str] = None) -> Shipment:
        shipment = ShipmentModel.objects.select_for_update().filter(
            id=shipment_id,
            deleted_at__isnull=True,
        ).first()
        if not shipment:
            raise ShipmentException.not_found()
        if shipment.status == 'packed':
            return ShipmentPersistenceMapper.from_entity(shipment)
        if shipment.status != 'pending':
            raise ShipmentException.invalid_status_transition(shipment.status, 'packed')

        now = timezone.now()
        shipment.status = 'packed'
        shipment.updated_by_id = actor_id
        shipment.save(update_fields=['status', 'updated_by', 'updated_at'])
        ShipmentEventModel.objects.create(
            shipment=shipment,
            status='packed',
            description=note or 'Products packed and ready for carrier handoff',
            event_time=now,
        )
        return ShipmentPersistenceMapper.from_entity(shipment)

    @transaction.atomic
    def handoff(self, shipment_id: str, actor_id: str, data: Dict[str, Any]) -> Shipment:
        shipment_ref = ShipmentModel.objects.filter(
            id=shipment_id,
            deleted_at__isnull=True,
        ).values('order_id').first()
        if not shipment_ref:
            raise ShipmentException.not_found()

        order = OrderModel.objects.select_for_update().filter(
            id=shipment_ref['order_id'],
            deleted_at__isnull=True,
        ).first()
        shipment = ShipmentModel.objects.select_for_update().filter(
            id=shipment_id,
            deleted_at__isnull=True,
        ).first()
        if not shipment:
            raise ShipmentException.not_found()
        if shipment.status == 'in_transit':
            return ShipmentPersistenceMapper.from_entity(shipment)
        if shipment.status != 'packed':
            raise ShipmentException.invalid_status_transition(shipment.status, 'in_transit')
        if order.status != 'processing':
            raise ShipmentException.order_not_ready(order.status, 'processing')

        now = timezone.now()
        shipment.status = 'in_transit'
        shipment.carrier_name = data['carrier_name']
        shipment.tracking_number = data['tracking_number']
        shipment.shipped_at = now
        shipment.updated_by_id = actor_id
        shipment.save(update_fields=[
            'status',
            'carrier_name',
            'tracking_number',
            'shipped_at',
            'updated_by',
            'updated_at',
        ])
        ShipmentEventModel.objects.create(
            shipment=shipment,
            status='in_transit',
            location=data.get('location'),
            description=data.get('note') or 'Package handed to carrier',
            event_time=now,
        )

        order.status = 'shipped'
        order.save(update_fields=['status', 'updated_at'])
        OrderStatusHistory.objects.create(
            order=order,
            from_status='processing',
            to_status='shipped',
            changed_by_id=actor_id,
            note=data.get('note') or f"Handed to {shipment.carrier_name}",
        )
        return ShipmentPersistenceMapper.from_entity(shipment)

    def list_admin(self, page: int, page_size: int) -> Tuple[List[Shipment], int]:
        qs = ShipmentModel.objects.filter(deleted_at__isnull=True).order_by('-created_at')
        total = qs.count()
        offset = (page - 1) * page_size
        models = list(qs[offset:offset + page_size])
        return [ShipmentPersistenceMapper.from_entity(model) for model in models], total

    @transaction.atomic
    def update_tracking(self, shipment_id: str, actor_id: str, data: Dict[str, Any]) -> Shipment:
        shipment = ShipmentModel.objects.select_for_update().filter(
            id=shipment_id,
            deleted_at__isnull=True,
        ).first()
        if not shipment:
            raise ShipmentException.not_found()

        update_fields = ['updated_by', 'updated_at']
        shipment.updated_by_id = actor_id
        for field in ('carrier_name', 'tracking_number'):
            if field in data:
                setattr(shipment, field, data[field])
                update_fields.append(field)
        shipment.save(update_fields=update_fields)
        return ShipmentPersistenceMapper.from_entity(shipment)

    @transaction.atomic
    def record_checkpoint(self, shipment_id: str, actor_id: str, data: Dict[str, Any]) -> ShipmentEvent:
        shipment = ShipmentModel.objects.select_for_update().filter(
            id=shipment_id,
            deleted_at__isnull=True,
        ).first()
        if not shipment:
            raise ShipmentException.not_found()
        if shipment.status not in {'in_transit', 'out_for_delivery'}:
            raise ShipmentException.invalid_status_transition(shipment.status, 'tracking_checkpoint')

        event = ShipmentEventModel.objects.create(
            shipment=shipment,
            status=shipment.status,
            location=data.get('location'),
            description=data['description'],
            event_time=data.get('event_time') or timezone.now(),
        )
        shipment.updated_by_id = actor_id
        shipment.save(update_fields=['updated_by', 'updated_at'])
        return ShipmentPersistenceMapper.event_from_entity(event)

    @transaction.atomic
    def mark_out_for_delivery(self, shipment_id: str, actor_id: str, data: Dict[str, Any]) -> Shipment:
        shipment_ref = ShipmentModel.objects.filter(
            id=shipment_id,
            deleted_at__isnull=True,
        ).values('order_id').first()
        if not shipment_ref:
            raise ShipmentException.not_found()

        order = OrderModel.objects.select_for_update().filter(
            id=shipment_ref['order_id'],
            deleted_at__isnull=True,
        ).first()
        shipment = ShipmentModel.objects.select_for_update().filter(
            id=shipment_id,
            deleted_at__isnull=True,
        ).first()
        if shipment.status == 'out_for_delivery':
            return ShipmentPersistenceMapper.from_entity(shipment)
        if shipment.status != 'in_transit':
            raise ShipmentException.invalid_status_transition(shipment.status, 'out_for_delivery')
        if order.status != 'shipped':
            raise ShipmentException.order_not_ready(order.status, 'shipped')

        now = timezone.now()
        shipment.status = 'out_for_delivery'
        shipment.updated_by_id = actor_id
        shipment.save(update_fields=['status', 'updated_by', 'updated_at'])
        ShipmentEventModel.objects.create(
            shipment=shipment,
            status='out_for_delivery',
            location=data.get('location'),
            description=data.get('note') or 'Package is out for delivery',
            event_time=now,
        )
        return ShipmentPersistenceMapper.from_entity(shipment)

    @transaction.atomic
    def confirm_delivery(self, shipment_id: str, user_id: str, note: Optional[str] = None) -> Shipment:
        shipment_ref = ShipmentModel.objects.filter(
            id=shipment_id,
            order__user_id=user_id,
            deleted_at__isnull=True,
        ).values('order_id').first()
        if not shipment_ref:
            raise ShipmentException.not_found()

        order = OrderModel.objects.select_for_update().filter(
            id=shipment_ref['order_id'],
            user_id=user_id,
            deleted_at__isnull=True,
        ).first()
        shipment = ShipmentModel.objects.select_for_update().filter(
            id=shipment_id,
            order=order,
            deleted_at__isnull=True,
        ).first()
        if shipment.status == 'delivered':
            return ShipmentPersistenceMapper.from_entity(shipment)
        if shipment.status != 'out_for_delivery':
            raise ShipmentException.invalid_status_transition(shipment.status, 'delivered')
        if order.status != 'shipped':
            raise ShipmentException.order_not_ready(order.status, 'shipped')

        now = timezone.now()
        shipment.status = 'delivered'
        shipment.delivered_at = now
        shipment.updated_by_id = user_id
        shipment.save(update_fields=['status', 'delivered_at', 'updated_by', 'updated_at'])
        ShipmentEventModel.objects.create(
            shipment=shipment,
            status='delivered',
            description=note or 'Delivery confirmed by customer',
            event_time=now,
        )

        other_open_shipments = ShipmentModel.objects.filter(
            order=order,
            deleted_at__isnull=True,
        ).exclude(status='delivered').exists()
        if not other_open_shipments:
            order.status = 'delivered'
            order.save(update_fields=['status', 'updated_at'])
            OrderStatusHistory.objects.create(
                order=order,
                from_status='shipped',
                to_status='delivered',
                changed_by_id=user_id,
                note=note or 'Delivery confirmed by customer',
            )

        return ShipmentPersistenceMapper.from_entity(shipment)
