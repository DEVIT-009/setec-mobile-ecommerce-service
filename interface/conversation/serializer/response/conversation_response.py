from dataclasses import dataclass
from typing import Optional


@dataclass
class ConversationResponse:
    id: Optional[str]
    customer_id: Optional[str]
    status: str
    store_id: Optional[str] = None
    order_id: Optional[str] = None
    last_message_at: Optional[str] = None
    created_at: Optional[str] = None

    def to_dict(self):
        return self.__dict__


@dataclass
class ConversationMessageResponse:
    id: Optional[str]
    conversation_id: Optional[str]
    sender_id: Optional[str]
    message_type: str
    body: Optional[str] = None
    attachment_url: Optional[str] = None
    read_at: Optional[str] = None
    created_at: Optional[str] = None

    def to_dict(self):
        return self.__dict__
