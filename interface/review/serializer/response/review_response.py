from dataclasses import dataclass
from typing import Optional


@dataclass
class ReviewResponse:
    id: str
    product_id: str
    user_id: str
    rating: int
    status: str
    title: Optional[str] = None
    body: Optional[str] = None
    order_item_id: Optional[str] = None
    created_at: Optional[str] = None

    def to_dict(self):
        return self.__dict__
