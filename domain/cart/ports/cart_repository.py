from abc import ABC, abstractmethod
from typing import Optional
from domain.cart.entity.cart import Cart, CartItem

class CartRepositoryInterface(ABC):
    @abstractmethod
    def get_active_cart(self, user_id: str) -> Optional[Cart]: pass
    @abstractmethod
    def create_cart(self, user_id: str) -> Cart: pass
    @abstractmethod
    def get_item(self, cart_item_id: str, cart_id: str) -> Optional[CartItem]: pass
    @abstractmethod
    def find_existing_item(self, cart_id: str, product_id: str, variant_id: Optional[str]) -> Optional[CartItem]: pass
    @abstractmethod
    def save_item(self, item: CartItem) -> CartItem: pass
    @abstractmethod
    def soft_delete_item(self, cart_item_id: str) -> None: pass
    @abstractmethod
    def select_all_items(self, cart_id: str, selected: bool) -> None: pass
    @abstractmethod
    def mark_checked_out(self, cart_id: str) -> None: pass
