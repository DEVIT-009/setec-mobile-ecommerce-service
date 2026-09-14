from decimal import Decimal
from typing import Dict, Any, Optional
from domain.cart.exception.cart_exception import CartException
from domain.cart.ports.cart_repository import CartRepositoryInterface
from domain.cart.service.cart_service import CartServiceInterface
from domain.cart.entity.cart import CartItem
from domain.product.ports.product_repository import ProductRepositoryInterface
from interface.cart.serializer.mapper.cart_controller_mapper import CartControllerMapper


class CartServiceFacade(CartServiceInterface):

    def __init__(self, cart_repo: CartRepositoryInterface, product_repo: ProductRepositoryInterface):
        self.cart_repo = cart_repo
        self.product_repo = product_repo

    def get_or_create_cart(self, user_id: str) -> Dict[str, Any]:
        cart = self.cart_repo.get_active_cart(user_id)
        if not cart:
            cart = self.cart_repo.create_cart(user_id)
        return CartControllerMapper.to_response(cart)

    def add_item(self, user_id: str, data: dict) -> Dict[str, Any]:
        cart = self.cart_repo.get_active_cart(user_id)
        if not cart:
            cart = self.cart_repo.create_cart(user_id)

        product_id = data['product_id']
        variant_id = data.get('product_variant_id')
        quantity = int(data.get('quantity', 1))

        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise CartException.product_not_found()

        # Check existing
        existing = self.cart_repo.find_existing_item(cart.id, product_id, variant_id)
        if existing:
            existing.quantity += quantity
            self.cart_repo.save_item(existing)
            updated_cart = self.cart_repo.get_active_cart(user_id)
            return CartControllerMapper.to_response(updated_cart)

        unit_price = Decimal(str(product.base_price))
        if variant_id:
            variant = next((v for v in product.variants if v.id == variant_id), None)
            if variant and variant.price is not None:
                unit_price = Decimal(str(variant.price))

        new_item = CartItem(
            cart_id=cart.id,
            product_id=product_id,
            product_variant_id=variant_id,
            quantity=quantity,
            unit_price_snapshot=unit_price,
            is_selected=True,
        )
        self.cart_repo.save_item(new_item)
        updated_cart = self.cart_repo.get_active_cart(user_id)
        return CartControllerMapper.to_response(updated_cart)

    def update_item(self, user_id: str, cart_item_id: str, data: dict) -> Dict[str, Any]:
        cart = self.cart_repo.get_active_cart(user_id)
        if not cart:
            raise CartException.not_found()

        item = self.cart_repo.get_item(cart_item_id, cart.id)
        if not item:
            raise CartException.item_not_found()

        if 'quantity' in data:
            item.quantity = data['quantity']
        if 'is_selected' in data:
            item.is_selected = data['is_selected']

        self.cart_repo.save_item(item)
        updated_cart = self.cart_repo.get_active_cart(user_id)
        return CartControllerMapper.to_response(updated_cart)

    def delete_item(self, user_id: str, cart_item_id: str) -> None:
        cart = self.cart_repo.get_active_cart(user_id)
        if not cart:
            raise CartException.not_found()

        item = self.cart_repo.get_item(cart_item_id, cart.id)
        if not item:
            raise CartException.item_not_found()

        self.cart_repo.soft_delete_item(cart_item_id)

    def select_all(self, user_id: str, selected: bool) -> Dict[str, Any]:
        cart = self.cart_repo.get_active_cart(user_id)
        if not cart:
            raise CartException.not_found()

        self.cart_repo.select_all_items(cart.id, selected)
        updated_cart = self.cart_repo.get_active_cart(user_id)
        return CartControllerMapper.to_response(updated_cart)

    def checkout_preview(self, user_id: str, shipping_address_id: Optional[str] = None) -> Dict[str, Any]:
        cart = self.cart_repo.get_active_cart(user_id)
        if not cart:
            raise CartException.not_found()
        res = CartControllerMapper.to_response(cart)
        return {
            "cart_id": cart.id,
            "shipping_address_id": shipping_address_id,
            "totals": res["totals"],
        }
