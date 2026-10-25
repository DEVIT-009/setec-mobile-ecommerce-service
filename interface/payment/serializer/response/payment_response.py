from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class PaymentResponse:
    id: str
    order_id: str
    batch_id: Optional[str]
    status: str
    amount: str
    currency: str
    provider: str
    provider_reference: Optional[str]
    failure_reason: Optional[str]
    paid_at: Optional[str]
    refunded_at: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]


@dataclass
class PaymentBatchResponse:
    id: str
    status: str
    total_amount: str
    currency: str
    provider: str
    provider_reference: Optional[str]
    failure_reason: Optional[str]
    order_ids: List[str]
    payments: List[Dict[str, Any]]
    paid_at: Optional[str]
    refunded_at: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]
