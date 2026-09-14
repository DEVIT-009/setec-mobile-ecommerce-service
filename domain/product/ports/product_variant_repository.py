from abc import ABC, abstractmethod
from typing import Optional, Tuple, List
from domain.product.entity.product import ProductVariant


class ProductVariantRepositoryInterface(ABC):

    @abstractmethod
    def list_by_product(self, product_id: str) -> List[ProductVariant]:
        pass

    @abstractmethod
    def get_by_id(self, variant_id: str) -> Optional[ProductVariant]:
        pass

    @abstractmethod
    def save(self, variant: ProductVariant, actor_id: Optional[str] = None) -> ProductVariant:
        pass

    @abstractmethod
    def soft_delete(self, variant_id: str, actor_id: Optional[str] = None) -> None:
        pass

    @abstractmethod
    def exists_sku(self, sku: str, exclude_id: Optional[str] = None) -> bool:
        pass
