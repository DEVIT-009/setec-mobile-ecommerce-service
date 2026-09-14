from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from domain.notification.entity.notification import Notification

class NotificationRepositoryInterface(ABC):
    @abstractmethod
    def list_by_user(self, user_id: str, page: int, page_size: int) -> Tuple[List[Notification], int]: pass
    @abstractmethod
    def unread_count(self, user_id: str) -> int: pass
    @abstractmethod
    def mark_read(self, notification_id: str, user_id: str) -> None: pass
    @abstractmethod
    def mark_all_read(self, user_id: str) -> None: pass
    @abstractmethod
    def soft_delete(self, notification_id: str, user_id: str) -> None: pass
    @abstractmethod
    def get_by_id(self, notification_id: str, user_id: str) -> Optional[Notification]: pass
