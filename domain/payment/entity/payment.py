from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List, Optional


@dataclass
class Payment:
    id: Optional[str] = None
    order_id: Optional[str] = None
    batch_id: Optional[str] = None
    user_id: Optional[str] = None
    status: str = "pending"
    amount: Decimal = Decimal("0")
    currency: str = "USD"
    provider: str = "internal_mock"
    provider_reference: Optional[str] = None
    idempotency_key: str = ""
    failure_reason: Optional[str] = None
    paid_at: Optional[datetime] = None
    refunded_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class PaymentBatch:
    id: Optional[str] = None
    user_id: Optional[str] = None
    status: str = "pending"
    total_amount: Decimal = Decimal("0")
    currency: str = "USD"
    provider: str = "internal_mock"
    provider_reference: Optional[str] = None
    idempotency_key: str = ""
    failure_reason: Optional[str] = None
    paid_at: Optional[datetime] = None
    refunded_at: Optional[datetime] = None
    payments: List[Payment] = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
