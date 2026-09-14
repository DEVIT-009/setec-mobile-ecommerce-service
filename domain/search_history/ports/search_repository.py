from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from domain.search_history.entity.search_history import SearchHistory

class SearchRepositoryInterface(ABC):
    @abstractmethod
    def save(self, record: SearchHistory) -> SearchHistory: pass
    @abstractmethod
    def list_by_user(self, user_id: str, page: int, page_size: int) -> Tuple[List[SearchHistory], int]: pass
    @abstractmethod
    def delete_by_id(self, search_id: str, user_id: str) -> bool: pass
    @abstractmethod
    def clear_all(self, user_id: str) -> None: pass
