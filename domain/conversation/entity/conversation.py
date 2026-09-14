from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

@dataclass
class ConversationMessage:
    id: Optional[str] = None
    conversation_id: Optional[str] = None
    sender_id: Optional[str] = None
    message_type: str = "text"
    body: Optional[str] = None
    attachment_url: Optional[str] = None
    read_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

@dataclass
class Conversation:
    id: Optional[str] = None
    customer_id: Optional[str] = None
    store_id: Optional[str] = None
    order_id: Optional[str] = None
    status: str = "open"
    last_message_at: Optional[datetime] = None
    unread_count: int = 0
    last_message_preview: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
