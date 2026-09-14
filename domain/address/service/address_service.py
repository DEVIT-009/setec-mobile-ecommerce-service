from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional


class AddressServiceInterface(ABC):

    @abstractmethod
    def list(self, user_id: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def create(self, user_id: str, data: dict, actor_id: Optional[str] = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get(self, address_id: str, user_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def update(self, address_id: str, user_id: str, data: dict, partial: bool = False, actor_id: Optional[str] = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    def delete(self, address_id: str, user_id: str, actor_id: Optional[str] = None) -> None:
        pass

    @abstractmethod
    def soft_delete(self, address_id: str, user_id: str, actor_id: Optional[str] = None) -> None:
        pass

    @abstractmethod
    def set_default(self, address_id: str, user_id: str, actor_id: Optional[str] = None) -> Dict[str, Any]:
        pass
