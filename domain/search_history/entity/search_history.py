from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Any


@dataclass
class SearchHistory:
    id: Optional[str] = None
    user_id: Optional[str] = None
    query: str = ""
    filters_json: Optional[Any] = None
    result_count: Optional[int] = None
    created_at: Optional[datetime] = None
