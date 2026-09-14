from abc import ABC, abstractmethod
from typing import List, Optional
from domain.address.entity.address import Address


class AddressRepositoryInterface(ABC):

    @abstractmethod
    def list_by_user(self, user_id: str) -> List[Address]:
        pass

    @abstractmethod
    def get_by_id(self, address_id: str, user_id: Optional[str] = None) -> Optional[Address]:
        pass

    @abstractmethod
    def create(self, address: Address, actor_id: Optional[str] = None) -> Address:
        pass

    @abstractmethod
    def update(self, address: Address, actor_id: Optional[str] = None) -> Address:
        pass

    @abstractmethod
    def soft_delete(self, address_id: str, user_id: Optional[str] = None, actor_id: Optional[str] = None) -> None:
        pass

    @abstractmethod
    def clear_default(self, user_id: str) -> None:
        pass

    @abstractmethod
    def save(self, address: Address, actor_id: Optional[str] = None) -> Address:
        """Backward-compatible save method."""
        pass
