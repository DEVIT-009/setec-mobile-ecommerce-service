from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class CartItemResponse:
    id: Optional[str]
    product: Dict[str, Any]
    quantity: int
    unit_price_snapshot: str
    line_total: str
    is_selected: bool
    variant: Optional[Dict[str, Any]] = None

    def to_dict(self):
        return self.__dict__


@dataclass
class CartTotalsResponse:
    selected_item_count: int = 0
    subtotal_amount: str = "0.00"
    shipping_amount: str = "0.00"
    discount_amount: str = "0.00"
    tax_amount: str = "0.00"
    total_amount: str = "0.00"
    currency: str = "USD"

    def to_dict(self):
        return self.__dict__


@dataclass
class CartResponse:
    id: Optional[str]
    status: str
    items: List[Dict[str, Any]]
    totals: Dict[str, Any]

    def to_dict(self):
        return self.__dict__
