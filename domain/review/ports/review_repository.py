from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from domain.review.entity.review import Review

class ReviewRepositoryInterface(ABC):
    @abstractmethod
    def create(self, review: Review, user_id: str) -> Review: pass
    @abstractmethod
    def get_by_id(self, review_id: str) -> Optional[Review]: pass
    @abstractmethod
    def save(self, review: Review) -> Review: pass
    @abstractmethod
    def soft_delete(self, review_id: str, user_id: str) -> None: pass
    @abstractmethod
    def list_by_product(self, product_id: str, page: int, page_size: int) -> Tuple[List[Review], int]: pass
    @abstractmethod
    def list_by_user(self, user_id: str, page: int, page_size: int) -> Tuple[List[Review], int]: pass
    @abstractmethod
    def list_published(self, product_id: Optional[str] = None, page: int = 1, page_size: int = 20) -> Tuple[List[Review], int]: pass
