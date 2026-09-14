from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class StoreServiceInterface(ABC):

    @abstractmethod
    def list_active(self, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        pass

    @abstractmethod
    def list_admin(self, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_by_id(self, store_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_by_slug(self, slug: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_admin(self, identifier: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def list_products(self, store_id: str, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        pass

    @abstractmethod
    def list_products_by_slug(self, slug: str, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        pass

    @abstractmethod
    def create(self, data: Dict[str, Any], actor_id: Optional[str] = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    def update(self, store_id: str, data: Dict[str, Any], partial: bool = False, actor_id: Optional[str] = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    def soft_delete(self, store_id: str, actor_id: Optional[str] = None) -> None:
        pass
