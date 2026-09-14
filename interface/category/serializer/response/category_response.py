from dataclasses import dataclass
from typing import Optional


@dataclass
class CategoryResponse:
    id: Optional[str]
    name: str
    slug: str
    parent_id: Optional[str] = None
    icon_url: Optional[str] = None
    image_url: Optional[str] = None
    sort_order: int = 0
    status: Optional[str] = None

    def to_dict(self):
        return self.__dict__

