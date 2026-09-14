from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from decimal import Decimal

@dataclass
class OrderItem:
    id: Optional[str] = None
    order_id: Optional[str] = None
    product_id: Optional[str] = None
    product_variant_id: Optional[str] = None
    product_name_snapshot: str = ""
    variant_name_snapshot: Optional[str] = None
    sku_snapshot: Optional[str] = None
    unit_price: Decimal = Decimal("0")
    quantity: int = 1
    line_total: Decimal = Decimal("0")

@dataclass
class OrderStatusEntry:
    id: Optional[str] = None
    order_id: Optional[str] = None
    from_status: Optional[str] = None
    to_status: str = ""
    note: Optional[str] = None
    created_at: Optional[datetime] = None

@dataclass
class Order:
    id: Optional[str] = None
    order_number: str = ""
    user_id: Optional[str] = None
    store_id: Optional[str] = None
    store_name: Optional[str] = None
    shipping_address_id: Optional[str] = None
    status: str = "pending"
    subtotal_amount: Decimal = Decimal("0")
    shipping_amount: Decimal = Decimal("0")
    discount_amount: Decimal = Decimal("0")
    tax_amount: Decimal = Decimal("0")
    total_amount: Decimal = Decimal("0")
    currency: str = "USD"
    placed_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None
    items: List[OrderItem] = field(default_factory=list)
    status_history: List[OrderStatusEntry] = field(default_factory=list)
    payment: None = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
