from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Any

@dataclass
class Notification:
    id: Optional[str] = None
    user_id: Optional[str] = None
    type: str = "system"
    title: str = ""
    body: Optional[str] = None
    data: Optional[Any] = None
    read_at: Optional[datetime] = None
    status: str = "queued"
    created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
