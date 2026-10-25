import hashlib
from typing import Optional

from django.db import transaction
from django.utils import timezone

from domain.payment.entity.payment import Payment, PaymentBatch
from domain.payment.exception.payment_exception import PaymentException
from domain.payment.ports.payment_repository import PaymentRepositoryInterface
from infrastructure.persistence.mapper.payment_persistence_mapper import PaymentPersistenceMapper
from infrastructure.persistence.models.order_model import Order as OrderModel
from infrastructure.persistence.models.order_status_history_model import OrderStatusHistory
from infrastructure.persistence.models.payment_model import Payment as PaymentModel, PaymentBatch as PaymentBatchModel
from infrastructure.persistence.repository.order_repository_impl import OrderRepositoryInterfaceImpl


class PaymentRepositoryInterfaceImpl(PaymentRepositoryInterface):
    @staticmethod
    def _confirm_order(order: OrderModel, user_id: str) -> None:
        old_status = order.status
        order.status = 'confirmed'
        order.save(update_fields=['status', 'updated_at'])

        OrderStatusHistory.objects.create(
            order=order,
            from_status=old_status,
            to_status='confirmed',
            changed_by_id=user_id,
            note='Payment succeeded via internal payment service',
        )

    @transaction.atomic
    def complete_internal_payment(
        self,
        order_id: str,
        user_id: str,
        idempotency_key: str,
        outcome: str = 'succeeded',
        failure_reason: Optional[str] = None,
    ) -> Payment:
        existing_by_key = PaymentModel.objects.filter(idempotency_key=idempotency_key).first()
        if existing_by_key:
            if str(existing_by_key.order_id) != order_id or str(existing_by_key.user_id) != user_id:
                raise PaymentException.idempotency_conflict()
            return PaymentPersistenceMapper.from_entity(existing_by_key)

        order = OrderModel.objects.select_for_update().filter(
            id=order_id,
            user_id=user_id,
            deleted_at__isnull=True,
        ).first()
        if not order:
            raise PaymentException.order_not_found()

        existing_for_order = PaymentModel.objects.filter(order=order).first()
        if existing_for_order:
            return PaymentPersistenceMapper.from_entity(existing_for_order)

        if order.status != 'pending':
            raise PaymentException.order_not_payable(order.status)

        now = timezone.now()
        normalized_failure_reason = (
            failure_reason or 'Payment failed in the internal payment simulator'
        ) if outcome == 'failed' else None
        payment_model = PaymentModel.objects.create(
            order=order,
            user_id=user_id,
            status=outcome,
            amount=order.total_amount,
            currency=order.currency,
            provider='internal_mock',
            idempotency_key=idempotency_key,
            failure_reason=normalized_failure_reason,
            paid_at=now if outcome == 'succeeded' else None,
        )
        payment_model.provider_reference = f"internal-{payment_model.id}"
        payment_model.save(update_fields=['provider_reference', 'updated_at'])

        if outcome == 'succeeded':
            self._confirm_order(order, user_id)
        else:
            OrderRepositoryInterfaceImpl().mark_failed(
                str(order.id),
                user_id,
                normalized_failure_reason,
            )

        return PaymentPersistenceMapper.from_entity(payment_model)

    @transaction.atomic
    def complete_internal_batch(
        self,
        order_ids: list[str],
        user_id: str,
        idempotency_key: str,
        outcome: str = 'succeeded',
        failure_reason: Optional[str] = None,
    ) -> PaymentBatch:
        requested_order_ids = sorted(set(order_ids))

        existing_batch = PaymentBatchModel.objects.filter(
            idempotency_key=idempotency_key
        ).first()
        if existing_batch:
            if str(existing_batch.user_id) != user_id:
                raise PaymentException.idempotency_conflict()
            existing_order_ids = sorted(
                str(order_id)
                for order_id in existing_batch.payments.values_list('order_id', flat=True)
            )
            if existing_order_ids != requested_order_ids:
                raise PaymentException.batch_idempotency_conflict()
            return PaymentPersistenceMapper.batch_from_entity(existing_batch)

        orders = list(OrderModel.objects.select_for_update().filter(
            id__in=requested_order_ids,
            user_id=user_id,
            deleted_at__isnull=True,
        ).order_by('id'))
        if len(orders) != len(requested_order_ids):
            raise PaymentException.order_not_found()

        not_payable = [
            {"order_id": str(order.id), "status": order.status}
            for order in orders
            if order.status != 'pending' or PaymentModel.objects.filter(order=order).exists()
        ]
        if not_payable:
            raise PaymentException.orders_not_payable(not_payable)

        currencies = {order.currency for order in orders}
        if len(currencies) != 1:
            raise PaymentException.currency_mismatch()

        now = timezone.now()
        normalized_failure_reason = (
            failure_reason or 'Payment failed in the internal payment simulator'
        ) if outcome == 'failed' else None
        currency = currencies.pop()
        batch_model = PaymentBatchModel.objects.create(
            user_id=user_id,
            status=outcome,
            total_amount=sum(order.total_amount for order in orders),
            currency=currency,
            provider='internal_mock',
            idempotency_key=idempotency_key,
            failure_reason=normalized_failure_reason,
            paid_at=now if outcome == 'succeeded' else None,
        )
        batch_model.provider_reference = f"internal-{batch_model.id}"
        batch_model.save(update_fields=['provider_reference', 'updated_at'])

        for order in orders:
            payment_key = hashlib.sha256(
                f"{idempotency_key}:{order.id}".encode('utf-8')
            ).hexdigest()
            payment_model = PaymentModel.objects.create(
                batch=batch_model,
                order=order,
                user_id=user_id,
                status=outcome,
                amount=order.total_amount,
                currency=order.currency,
                provider='internal_mock',
                idempotency_key=f"batch:{payment_key}",
                failure_reason=normalized_failure_reason,
                paid_at=now if outcome == 'succeeded' else None,
            )
            payment_model.provider_reference = f"internal-{payment_model.id}"
            payment_model.save(update_fields=['provider_reference', 'updated_at'])
            if outcome == 'succeeded':
                self._confirm_order(order, user_id)
            else:
                OrderRepositoryInterfaceImpl().mark_failed(
                    str(order.id),
                    user_id,
                    normalized_failure_reason,
                )

        return PaymentPersistenceMapper.batch_from_entity(batch_model)

    def get_by_order(self, order_id: str, user_id: str) -> Optional[Payment]:
        order_exists = OrderModel.objects.filter(
            id=order_id,
            user_id=user_id,
            deleted_at__isnull=True,
        ).exists()
        if not order_exists:
            raise PaymentException.order_not_found()

        payment_model = PaymentModel.objects.filter(order_id=order_id, user_id=user_id).first()
        return PaymentPersistenceMapper.from_entity(payment_model)
