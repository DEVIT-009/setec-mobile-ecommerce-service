from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Favorite:
    id: Optional[str] = None
    user_id: Optional[str] = None
    product_id: Optional[str] = None
    created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
