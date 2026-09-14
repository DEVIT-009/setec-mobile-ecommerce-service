from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from domain.tag.entity.tag import Tag


class TagRepositoryInterface(ABC):

    @abstractmethod
    def list(self, page: int, page_size: int) -> Tuple[List[Tag], int]:
        pass

    @abstractmethod
    def get_by_id(self, tag_id: str) -> Optional[Tag]:
        pass

    @abstractmethod
    def exists_by_slug(self, slug: str, exclude_id: Optional[str] = None) -> bool:
        pass

    @abstractmethod
    def exists_by_name(self, name: str, exclude_id: Optional[str] = None) -> bool:
        pass

    @abstractmethod
    def create(self, tag: Tag) -> Tag:
        pass

    @abstractmethod
    def update(self, tag: Tag) -> Tag:
        pass

    @abstractmethod
    def delete(self, tag_id: str) -> None:
        pass
