from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class OrderItemResponse:
    id: Optional[str]
    product_id: Optional[str]
    product_name: str
    unit_price: str
    quantity: int
    line_total: str
    product_variant_id: Optional[str] = None
    variant_name: Optional[str] = None
    sku: Optional[str] = None

    def to_dict(self):
        return self.__dict__


@dataclass
class OrderSummaryResponse:
    id: Optional[str]
    order_number: str
    status: str
    total_amount: str
    currency: str
    item_count: int
    store: Optional[Dict[str, Any]] = None
    placed_at: Optional[str] = None

    def to_dict(self):
        return self.__dict__


@dataclass
class OrderDetailResponse:
    id: Optional[str]
    order_number: str
    status: str
    subtotal_amount: str
    shipping_amount: str
    discount_amount: str
    tax_amount: str
    total_amount: str
    currency: str
    items: List[Dict[str, Any]]
    store: Optional[Dict[str, Any]] = None
    shipping_address_id: Optional[str] = None
    payment: Optional[Dict[str, Any]] = None
    shipments: Optional[List[Any]] = None
    status_history: Optional[List[Dict[str, Any]]] = None
    placed_at: Optional[str] = None
    cancelled_at: Optional[str] = None

    def to_dict(self):
        return self.__dict__
