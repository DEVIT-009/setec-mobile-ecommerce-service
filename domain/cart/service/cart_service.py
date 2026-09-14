from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class CartServiceInterface(ABC):
    @abstractmethod
    def get_or_create_cart(self, user_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def add_item(self, user_id: str, data: dict) -> Dict[str, Any]:
        pass

    @abstractmethod
    def update_item(self, user_id: str, cart_item_id: str, data: dict) -> Dict[str, Any]:
        pass

    @abstractmethod
    def delete_item(self, user_id: str, cart_item_id: str) -> None:
        pass

    @abstractmethod
    def select_all(self, user_id: str, selected: bool) -> Dict[str, Any]:
        pass

    @abstractmethod
    def checkout_preview(self, user_id: str, shipping_address_id: Optional[str] = None) -> Dict[str, Any]:
        pass
