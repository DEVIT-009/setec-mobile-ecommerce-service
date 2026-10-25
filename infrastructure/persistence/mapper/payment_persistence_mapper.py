from typing import Optional

from domain.payment.entity.payment import Payment as DomainPayment, PaymentBatch as DomainPaymentBatch
from infrastructure.persistence.models.payment_model import Payment as PaymentModel, PaymentBatch as PaymentBatchModel


class PaymentPersistenceMapper:
    @staticmethod
    def from_entity(entity: Optional[PaymentModel]) -> Optional[DomainPayment]:
        if entity is None:
            return None
        return DomainPayment(
            id=str(entity.id),
            order_id=str(entity.order_id),
            batch_id=str(entity.batch_id) if entity.batch_id else None,
            user_id=str(entity.user_id),
            status=entity.status,
            amount=entity.amount,
            currency=entity.currency,
            provider=entity.provider,
            provider_reference=entity.provider_reference,
            idempotency_key=entity.idempotency_key,
            failure_reason=entity.failure_reason,
            paid_at=entity.paid_at,
            refunded_at=entity.refunded_at,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @staticmethod
    def batch_from_entity(entity: Optional[PaymentBatchModel]) -> Optional[DomainPaymentBatch]:
        if entity is None:
            return None
        return DomainPaymentBatch(
            id=str(entity.id),
            user_id=str(entity.user_id),
            status=entity.status,
            total_amount=entity.total_amount,
            currency=entity.currency,
            provider=entity.provider,
            provider_reference=entity.provider_reference,
            idempotency_key=entity.idempotency_key,
            paid_at=entity.paid_at,
            refunded_at=entity.refunded_at,
            payments=[
                PaymentPersistenceMapper.from_entity(payment)
                for payment in entity.payments.order_by('created_at')
            ],
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
