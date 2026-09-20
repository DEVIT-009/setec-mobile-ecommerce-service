from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class SearchHistoryResponse:
    id: Optional[str]
    query: str
    filters_json: Optional[Any] = None
    result_count: Optional[int] = None
    created_at: Optional[str] = None
