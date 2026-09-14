from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

@dataclass
class SupportMessage:
    id: Optional[str] = None
    ticket_id: Optional[str] = None
    sender_id: Optional[str] = None
    body: str = ""
    attachment_url: Optional[str] = None
    created_at: Optional[datetime] = None

@dataclass
class SupportTicket:
    id: Optional[str] = None
    user_id: Optional[str] = None
    order_id: Optional[str] = None
    subject: str = ""
    category: str = "other"
    status: str = "open"
    priority: str = "normal"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
