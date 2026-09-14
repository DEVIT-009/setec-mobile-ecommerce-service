from abc import ABC, abstractmethod
from typing import Dict, Any

class FavoriteServiceInterface(ABC):
    @abstractmethod
    def list(self, user_id: str, page: int = 1, page_size: int = 20) -> Dict[str, Any]: pass
    @abstractmethod
    def add(self, user_id: str, product_id: str) -> Dict[str, Any]: pass
    @abstractmethod
    def remove(self, user_id: str, product_id: str) -> None: pass
    @abstractmethod
    def get_state(self, user_id: str, product_id: str) -> Dict[str, Any]: pass
