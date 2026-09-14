from abc import ABC, abstractmethod
from typing import Dict, Any

class NotificationServiceInterface(ABC):
    @abstractmethod
    def list(self, user_id: str, page: int = 1, page_size: int = 20) -> Dict[str, Any]: pass
    @abstractmethod
    def unread_count(self, user_id: str) -> Dict[str, Any]: pass
    @abstractmethod
    def mark_read(self, user_id: str, notification_id: str) -> None: pass
    @abstractmethod
    def mark_all_read(self, user_id: str) -> None: pass
    @abstractmethod
    def delete(self, user_id: str, notification_id: str) -> None: pass
    @abstractmethod
    def create_admin_notification(self, data: dict) -> Dict[str, Any]: pass
