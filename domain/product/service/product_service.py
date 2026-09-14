from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List

class ProductServiceInterface(ABC):

    @abstractmethod
    def list_active(self, filters: dict, page: int, page_size: int, user_id: Optional[str] = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    def list_admin(self, filters: dict, page: int, page_size: int) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_by_id(self, product_id: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_by_store_and_slug(self, store_slug: str, product_slug: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_images(self, product_id: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_variants(self, product_id: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def list_tags(self, page: int, page_size: int) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_reviews(self, product_id: str, page: int, page_size: int) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_favorite_state(self, product_id: str, user_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def create(self, data: Dict[str, Any], actor_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def update(self, product_id: str, data: Dict[str, Any], actor_id: str, partial: bool = False) -> Dict[str, Any]:
        pass

    @abstractmethod
    def soft_delete(self, product_id: str, actor_id: str) -> None:
        pass
