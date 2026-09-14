from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List


class ProductVariantServiceInterface(ABC):

    @abstractmethod
    def list_by_product(self, product_id: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_by_id(self, variant_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def create(self, data: Dict[str, Any], actor_id: Optional[str] = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    def update(self, variant_id: str, data: Dict[str, Any], actor_id: Optional[str] = None, partial: bool = False) -> Dict[str, Any]:
        pass

    @abstractmethod
    def soft_delete(self, variant_id: str, actor_id: Optional[str] = None) -> None:
        pass
