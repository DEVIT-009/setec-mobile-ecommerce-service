from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Review:
    id: Optional[str] = None
    user_id: Optional[str] = None
    product_id: Optional[str] = None
    order_item_id: Optional[str] = None
    rating: int = 5
    title: Optional[str] = None
    body: Optional[str] = None
    status: str = "pending"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
