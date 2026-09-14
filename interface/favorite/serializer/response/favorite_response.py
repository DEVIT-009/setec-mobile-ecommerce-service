from dataclasses import dataclass
from typing import Optional


@dataclass
class FavoriteResponse:
    id: Optional[str]
    user_id: Optional[str]
    product_id: Optional[str]
    created_at: Optional[str] = None

    def to_dict(self):
        return self.__dict__
