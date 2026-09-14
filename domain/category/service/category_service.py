from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class CategoryServiceInterface(ABC):

    @abstractmethod
    def list_active(self, parent_id: Optional[str] = None) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def list_admin(self, parent_id: Optional[str] = None) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_tree(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_by_slug(self, slug: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_by_id(self, category_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_admin(self, identifier: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def create(self, data: dict, actor_id: Optional[str] = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    def update(self, category_id: str, data: dict, partial: bool = False, actor_id: Optional[str] = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    def soft_delete(self, category_id: str, actor_id: Optional[str] = None) -> None:
        pass

