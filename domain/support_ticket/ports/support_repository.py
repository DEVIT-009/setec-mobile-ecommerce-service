from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from domain.support_ticket.entity.support_ticket import SupportTicket, SupportMessage

class SupportRepositoryInterface(ABC):
    @abstractmethod
    def list_by_user(self, user_id: str, page: int, page_size: int) -> Tuple[List[SupportTicket], int]: pass
    @abstractmethod
    def create(self, ticket: SupportTicket) -> SupportTicket: pass
    @abstractmethod
    def get_by_id(self, ticket_id: str, user_id: str) -> Optional[SupportTicket]: pass
    @abstractmethod
    def save(self, ticket: SupportTicket) -> SupportTicket: pass
    @abstractmethod
    def list_messages(self, ticket_id: str, page: int, page_size: int) -> Tuple[List[SupportMessage], int]: pass
    @abstractmethod
    def add_message(self, msg: SupportMessage) -> SupportMessage: pass
