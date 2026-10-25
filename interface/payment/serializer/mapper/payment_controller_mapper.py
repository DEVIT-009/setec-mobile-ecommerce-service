from dataclasses import asdict
from typing import Any, Dict

from domain.payment.entity.payment import Payment, PaymentBatch
from interface.payment.serializer.response.payment_response import PaymentBatchResponse, PaymentResponse


class PaymentControllerMapper:
    @staticmethod
    def to_response(payment: Payment) -> Dict[str, Any]:
        return asdict(PaymentResponse(
            id=str(payment.id),
            order_id=str(payment.order_id),
            batch_id=str(payment.batch_id) if payment.batch_id else None,
            status=payment.status,
            amount=str(payment.amount),
            currency=payment.currency,
            provider=payment.provider,
            provider_reference=payment.provider_reference,
            failure_reason=payment.failure_reason,
            paid_at=payment.paid_at.isoformat() if payment.paid_at else None,
            refunded_at=payment.refunded_at.isoformat() if payment.refunded_at else None,
            created_at=payment.created_at.isoformat() if payment.created_at else None,
            updated_at=payment.updated_at.isoformat() if payment.updated_at else None,
        ))

    @staticmethod
    def to_batch_response(batch: PaymentBatch) -> Dict[str, Any]:
        payments = [PaymentControllerMapper.to_response(payment) for payment in batch.payments]
        return asdict(PaymentBatchResponse(
            id=str(batch.id),
            status=batch.status,
            total_amount=str(batch.total_amount),
            currency=batch.currency,
            provider=batch.provider,
            provider_reference=batch.provider_reference,
            failure_reason=batch.failure_reason,
            order_ids=[payment["order_id"] for payment in payments],
            payments=payments,
            paid_at=batch.paid_at.isoformat() if batch.paid_at else None,
            refunded_at=batch.refunded_at.isoformat() if batch.refunded_at else None,
            created_at=batch.created_at.isoformat() if batch.created_at else None,
            updated_at=batch.updated_at.isoformat() if batch.updated_at else None,
        ))
