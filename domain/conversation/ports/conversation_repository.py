from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from domain.conversation.entity.conversation import Conversation, ConversationMessage

class ConversationRepositoryInterface(ABC):
    @abstractmethod
    def list_by_user(self, user_id: str, page: int, page_size: int) -> Tuple[List[Conversation], int]: pass
    @abstractmethod
    def create(self, conv: Conversation) -> Conversation: pass
    @abstractmethod
    def get_by_id(self, conversation_id: str, user_id: str) -> Optional[Conversation]: pass
    @abstractmethod
    def save(self, conv: Conversation) -> Conversation: pass
    @abstractmethod
    def list_messages(self, conversation_id: str, page: int, page_size: int) -> Tuple[List[ConversationMessage], int]: pass
    @abstractmethod
    def send_message(self, msg: ConversationMessage) -> ConversationMessage: pass
    @abstractmethod
    def mark_message_read(self, message_id: str) -> None: pass
