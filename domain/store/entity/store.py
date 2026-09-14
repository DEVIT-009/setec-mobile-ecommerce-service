from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Store:
    id: Optional[str] = None
    owner_id: Optional[str] = None
    name: str = ""
    slug: str = ""
    description: Optional[str] = None
    logo_url: Optional[str] = None
    banner_url: Optional[str] = None
    status: str = "active"
    rating_average: float = 0.0
    rating_count: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
