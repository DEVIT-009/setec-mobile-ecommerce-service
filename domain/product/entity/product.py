from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

@dataclass
class ProductImage:
    id: Optional[str] = None
    product_id: Optional[str] = None
    image_url: str = ""
    alt_text: Optional[str] = None
    sort_order: int = 0
    is_primary: bool = False

@dataclass
class VariantOption:
    id: Optional[str] = None
    variant_id: Optional[str] = None
    name: str = ""
    value: str = ""


@dataclass
class ProductVariant:
    id: Optional[str] = None
    product_id: Optional[str] = None
    sku: Optional[str] = None
    name: str = ""
    price: Optional[float] = None
    stock_quantity: int = 0
    status: str = "active"
    options: List[VariantOption] = field(default_factory=list)

@dataclass
class Tag:
    id: Optional[str] = None
    name: str = ""
    slug: str = ""

@dataclass
class Product:
    id: Optional[str] = None
    store_id: Optional[str] = None
    store_name: Optional[str] = None
    store_slug: Optional[str] = None
    category_id: Optional[str] = None
    category_name: Optional[str] = None
    name: str = ""
    slug: str = ""
    description: Optional[str] = None
    base_price: float = 0.0
    compare_at_price: Optional[float] = None
    currency: str = "USD"
    sku: Optional[str] = None
    status: str = "draft"
    rating_average: float = 0.0
    rating_count: int = 0
    sold_count: int = 0
    primary_image_url: Optional[str] = None
    images: List[ProductImage] = field(default_factory=list)
    variants: List[ProductVariant] = field(default_factory=list)
    tags: List[Tag] = field(default_factory=list)
    is_favorite: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
