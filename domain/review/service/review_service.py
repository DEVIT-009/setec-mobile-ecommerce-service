from abc import ABC, abstractmethod
from typing import Dict, Any

class ReviewServiceInterface(ABC):
    @abstractmethod
    def create(self, user_id: str, data: dict) -> Dict[str, Any]: pass
    @abstractmethod
    def update(self, user_id: str, review_id: str, data: dict) -> Dict[str, Any]: pass
    @abstractmethod
    def delete(self, user_id: str, review_id: str) -> None: pass
    @abstractmethod
    def list_by_user(self, user_id: str, page: int, page_size: int) -> Dict[str, Any]: pass
    @abstractmethod
    def list_admin(self, filters: dict, page: int, page_size: int) -> Dict[str, Any]: pass
    @abstractmethod
    def set_status(self, review_id: str, status: str) -> Dict[str, Any]: pass
    @abstractmethod
    def get_admin(self, review_id: str) -> Dict[str, Any]: pass
    @abstractmethod
    def update_admin(self, review_id: str, data: dict, actor_id: str = None) -> Dict[str, Any]: pass
    @abstractmethod
    def delete_admin(self, review_id: str, actor_id: str = None) -> None: pass
    @abstractmethod
    def list_public(self, product_id: str = None, page: int = 1, page_size: int = 20) -> Dict[str, Any]: pass
    @abstractmethod
    def get_public(self, review_id: str) -> Dict[str, Any]: pass

