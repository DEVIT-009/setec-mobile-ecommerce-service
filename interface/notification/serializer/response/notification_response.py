from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class NotificationResponse:
    id: Optional[str]
    type: str
    title: str
    body: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    read_at: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[str] = None

    def to_dict(self):
        return self.__dict__
