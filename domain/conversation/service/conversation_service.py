from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class ConversationServiceInterface(ABC):
    @abstractmethod
    def list_conversations(self, user_id: str, page: int = 1, page_size: int = 20) -> Dict[str, Any]: pass
    @abstractmethod
    def create_conversation(self, user_id: str, data: dict) -> Dict[str, Any]: pass
    @abstractmethod
    def get_conversation(self, user_id: str, conversation_id: str) -> Dict[str, Any]: pass
    @abstractmethod
    def update_conversation(self, user_id: str, conversation_id: str, data: dict) -> Dict[str, Any]: pass
    @abstractmethod
    def list_messages(self, user_id: str, conversation_id: str, page: int = 1, page_size: int = 30) -> Dict[str, Any]: pass
    @abstractmethod
    def send_message(self, user_id: str, conversation_id: str, data: dict) -> Dict[str, Any]: pass
    @abstractmethod
    def mark_message_read(self, user_id: str, message_id: str) -> None: pass
