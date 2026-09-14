from abc import ABC, abstractmethod
from typing import Optional, Tuple, List
from domain.product.entity.product import Product, ProductImage, ProductVariant, Tag


class ProductRepositoryInterface(ABC):
    @abstractmethod
    def list_active(self, filters: dict, page: int, page_size: int, user_id: Optional[str] = None) -> Tuple[List[Product], int]: pass
    @abstractmethod
    def list_all(self, filters: dict, page: int, page_size: int) -> Tuple[List[Product], int]: pass
    @abstractmethod
    def get_by_id(self, product_id: str, user_id: Optional[str] = None) -> Optional[Product]: pass
    @abstractmethod
    def get_by_store_and_slug(self, store_slug: str, product_slug: str, user_id: Optional[str] = None) -> Optional[Product]: pass
    @abstractmethod
    def get_images(self, product_id: str) -> List[ProductImage]: pass
    @abstractmethod
    def get_variants(self, product_id: str) -> List[ProductVariant]: pass
    @abstractmethod
    def list_tags(self, page: int, page_size: int) -> Tuple[List[Tag], int]: pass
    @abstractmethod
    def exists_by_store_and_slug(self, store_id: str, slug: str, exclude_id: Optional[str] = None) -> bool: pass
    @abstractmethod
    def save(self, product: Product, actor_id: Optional[str] = None) -> Product: pass
    @abstractmethod
    def soft_delete(self, product_id: str, actor_id: Optional[str] = None) -> None: pass
    @abstractmethod
    def is_favorite(self, product_id: str, user_id: str) -> bool: pass
