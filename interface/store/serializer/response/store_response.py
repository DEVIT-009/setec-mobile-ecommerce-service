from dataclasses import dataclass
from typing import Optional


@dataclass
class StoreResponse:
    id: Optional[str]
    name: str
    slug: str
    owner_id: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    banner_url: Optional[str] = None
    status: Optional[str] = None
    rating_average: float = 0.0
    rating_count: int = 0
    created_at: Optional[str] = None

    def to_dict(self):
        return self.__dict__
