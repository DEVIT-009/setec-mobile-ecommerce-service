from abc import ABC, abstractmethod
from typing import Dict, Any


class SearchServiceInterface(ABC):
    @abstractmethod
    def record(self, user_id: str, data: dict) -> Dict[str, Any]: pass

    @abstractmethod
    def list(self, user_id: str, page: int = 1, page_size: int = 20) -> Dict[str, Any]: pass

    @abstractmethod
    def delete_one(self, search_id: str, user_id: str) -> None: pass

    @abstractmethod
    def clear_all(self, user_id: str) -> None: pass
