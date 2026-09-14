from abc import ABC, abstractmethod
from typing import Dict, Any

class SupportServiceInterface(ABC):
    @abstractmethod
    def list_tickets(self, user_id: str, page: int = 1, page_size: int = 20) -> Dict[str, Any]: pass
    @abstractmethod
    def create_ticket(self, user_id: str, data: dict) -> Dict[str, Any]: pass
    @abstractmethod
    def get_ticket(self, user_id: str, ticket_id: str) -> Dict[str, Any]: pass
    @abstractmethod
    def update_ticket(self, user_id: str, ticket_id: str, data: dict) -> Dict[str, Any]: pass
    @abstractmethod
    def list_messages(self, user_id: str, ticket_id: str, page: int = 1, page_size: int = 30) -> Dict[str, Any]: pass
    @abstractmethod
    def add_message(self, user_id: str, ticket_id: str, data: dict) -> Dict[str, Any]: pass
    @abstractmethod
    def list_admin_tickets(self, filters: dict, page: int = 1, page_size: int = 20) -> Dict[str, Any]: pass
    @abstractmethod
    def update_admin_ticket(self, ticket_id: str, data: dict) -> Dict[str, Any]: pass
