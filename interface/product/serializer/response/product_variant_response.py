from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class VariantOptionResponse:
    name: str
    value: str

    def to_dict(self):
        return self.__dict__


@dataclass
class ProductVariantDetailResponse:
    id: Optional[str]
    product_id: Optional[str]
    name: str
    sku: Optional[str]
    stock_quantity: int
    status: str
    price: Optional[str] = None
    options: Optional[List[Dict[str, Any]]] = None

    def to_dict(self):
        return self.__dict__
