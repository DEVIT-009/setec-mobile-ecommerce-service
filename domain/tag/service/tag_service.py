from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class TagServiceInterface(ABC):

    @abstractmethod
    def list(self, page: int, page_size: int) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get(self, tag_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def create(self, data: dict, actor_id: Optional[str] = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    def update(self, tag_id: str, data: dict, partial: bool = False, actor_id: Optional[str] = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    def delete(self, tag_id: str, actor_id: Optional[str] = None) -> None:
        pass
