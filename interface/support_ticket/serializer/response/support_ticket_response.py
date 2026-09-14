from dataclasses import dataclass
from typing import Optional


@dataclass
class SupportTicketResponse:
    id: Optional[str]
    user_id: Optional[str]
    subject: str
    category: str
    status: str
    priority: str
    order_id: Optional[str] = None
    created_at: Optional[str] = None

    def to_dict(self):
        return self.__dict__


@dataclass
class SupportMessageResponse:
    id: Optional[str]
    ticket_id: Optional[str]
    sender_id: Optional[str]
    body: str
    attachment_url: Optional[str] = None
    created_at: Optional[str] = None

    def to_dict(self):
        return self.__dict__
