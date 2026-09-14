from abc import ABC, abstractmethod
from typing import Optional, List
from domain.product.entity.product import VariantOption


class VariantOptionRepositoryInterface(ABC):

    @abstractmethod
    def list_by_variant(self, variant_id: str) -> List[VariantOption]:
        pass

    @abstractmethod
    def get_by_id(self, option_id: str) -> Optional[VariantOption]:
        pass

    @abstractmethod
    def save(self, option: VariantOption) -> VariantOption:
        pass

    @abstractmethod
    def delete(self, option_id: str) -> None:
        pass

    @abstractmethod
    def exists_name_in_variant(self, variant_id: str, name: str, exclude_id: Optional[str] = None) -> bool:
        pass
