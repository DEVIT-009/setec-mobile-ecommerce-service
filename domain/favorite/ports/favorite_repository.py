from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from domain.favorite.entity.favorite import Favorite

class FavoriteRepositoryInterface(ABC):
    @abstractmethod
    def list_by_user(self, user_id: str, page: int, page_size: int) -> Tuple[List[Favorite], int]: pass
    @abstractmethod
    def get(self, user_id: str, product_id: str) -> Optional[Favorite]: pass
    @abstractmethod
    def save(self, favorite: Favorite) -> Favorite: pass
    @abstractmethod
    def remove(self, user_id: str, product_id: str) -> bool: pass
