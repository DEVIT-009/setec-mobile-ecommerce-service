from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from decimal import Decimal

@dataclass
class CartItem:
    id: Optional[str] = None
    cart_id: Optional[str] = None
    product_id: Optional[str] = None
    product_name: Optional[str] = None
    primary_image_url: Optional[str] = None
    product_variant_id: Optional[str] = None
    variant_name: Optional[str] = None
    quantity: int = 1
    unit_price_snapshot: Decimal = Decimal("0")
    is_selected: bool = True
    deleted_at: Optional[datetime] = None

@dataclass
class CartTotals:
    selected_item_count: int = 0
    subtotal_amount: Decimal = Decimal("0")
    shipping_amount: Decimal = Decimal("0")
    discount_amount: Decimal = Decimal("0")
    tax_amount: Decimal = Decimal("0")
    total_amount: Decimal = Decimal("0")
    currency: str = "USD"

@dataclass
class Cart:
    id: Optional[str] = None
    user_id: Optional[str] = None
    status: str = "active"
    items: List[CartItem] = field(default_factory=list)
    totals: Optional[CartTotals] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
