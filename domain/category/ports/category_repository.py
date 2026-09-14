from abc import ABC, abstractmethod
from typing import List, Optional
from domain.category.entity.category import Category


class CategoryRepositoryInterface(ABC):

    @abstractmethod
    def list_active(self, parent_id: Optional[str] = None) -> List[Category]:
        pass

    @abstractmethod
    def list_admin(self, parent_id: Optional[str] = None) -> List[Category]:
        pass

    @abstractmethod
    def get_by_slug(self, slug: str) -> Optional[Category]:
        pass

    @abstractmethod
    def get_by_id(self, category_id: str) -> Optional[Category]:
        pass

    @abstractmethod
    def get_children(self, parent_id: str) -> List[Category]:
        pass

    @abstractmethod
    def get_root_categories(self) -> List[Category]:
        pass

    @abstractmethod
    def exists_by_slug(self, slug: str, exclude_id: Optional[str] = None) -> bool:
        pass

    @abstractmethod
    def create(self, category: Category, actor_id: Optional[str] = None) -> Category:
        pass

    @abstractmethod
    def update(self, category: Category, actor_id: Optional[str] = None) -> Category:
        pass

    @abstractmethod
    def soft_delete(self, category_id: str, actor_id: Optional[str] = None) -> None:
        pass



