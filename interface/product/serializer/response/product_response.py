from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class ProductImageResponse:
    id: Optional[str]
    image_url: str
    alt_text: Optional[str] = None
    sort_order: int = 0
    is_primary: bool = False

    def to_dict(self):
        return self.__dict__


@dataclass
class ProductVariantResponse:
    id: Optional[str]
    name: str
    sku: Optional[str]
    stock_quantity: int
    status: str
    price: Optional[str] = None
    options: Optional[List[Dict[str, Any]]] = None

    def to_dict(self):
        return self.__dict__


@dataclass
class TagResponse:
    id: Optional[str]
    name: str
    slug: str

    def to_dict(self):
        return self.__dict__


@dataclass
class ProductCardResponse:
    id: Optional[str]
    name: str
    slug: str
    base_price: str
    currency: str
    rating_average: float
    rating_count: int
    sold_count: int
    status: str
    compare_at_price: Optional[str] = None
    primary_image_url: Optional[str] = None
    store: Optional[Dict[str, Any]] = None
    is_favorite: bool = False

    def to_dict(self):
        return self.__dict__


@dataclass
class ProductDetailResponse:
    id: Optional[str]
    name: str
    slug: str
    base_price: str
    currency: str
    rating_average: float
    rating_count: int
    sold_count: int
    status: str
    description: Optional[str] = None
    sku: Optional[str] = None
    compare_at_price: Optional[str] = None
    primary_image_url: Optional[str] = None
    store: Optional[Dict[str, Any]] = None
    is_favorite: bool = False
    category: Optional[Dict[str, Any]] = None
    images: Optional[List[Dict[str, Any]]] = None
    variants: Optional[List[Dict[str, Any]]] = None
    tags: Optional[List[Dict[str, Any]]] = None

    def to_dict(self):
        return self.__dict__
