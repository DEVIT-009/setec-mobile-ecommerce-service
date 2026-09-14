from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List


class VariantOptionServiceInterface(ABC):

    @abstractmethod
    def list_by_variant(self, variant_id: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_by_id(self, option_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def update(self, option_id: str, data: Dict[str, Any], partial: bool = False) -> Dict[str, Any]:
        pass

    @abstractmethod
    def delete(self, option_id: str) -> None:
        pass
