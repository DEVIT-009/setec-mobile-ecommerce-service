
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List


@dataclass
class Category:
    id: Optional[str] = None
    parent_id: Optional[str] = None
    name: str = ""
    slug: str = ""
    icon_url: Optional[str] = None
    image_url: Optional[str] = None
    sort_order: int = 0
    status: str = "active"
    children: List['Category'] = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
