from abc import ABC, abstractmethod
from typing import Optional, List, Tuple
from domain.store.entity.store import Store


class StoreRepositoryInterface(ABC):

    @abstractmethod
    def list_active(self, page: int = 1, page_size: int = 20) -> Tuple[List[Store], int]:
        pass

    @abstractmethod
    def list_all(self, page: int = 1, page_size: int = 20) -> Tuple[List[Store], int]:
        pass

    @abstractmethod
    def get_by_slug(self, slug: str) -> Optional[Store]:
        pass

    @abstractmethod
    def get_by_id(self, store_id: str) -> Optional[Store]:
        pass

    @abstractmethod
    def exists_by_slug(self, slug: str, exclude_id: Optional[str] = None) -> bool:
        pass

    @abstractmethod
    def create(self, store: Store, actor_id: Optional[str] = None) -> Store:
        pass

    @abstractmethod
    def update(self, store: Store, actor_id: Optional[str] = None) -> Store:
        pass

    @abstractmethod
    def soft_delete(self, store_id: str, actor_id: Optional[str] = None) -> None:
        pass

    @abstractmethod
    def save(self, store: Store, actor_id: Optional[str] = None) -> Store:
        pass
