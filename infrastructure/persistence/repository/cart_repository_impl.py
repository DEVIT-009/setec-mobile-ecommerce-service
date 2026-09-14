from typing import Optional
from domain.cart.ports.cart_repository import CartRepositoryInterface
from domain.cart.entity.cart import Cart, CartItem
from infrastructure.persistence.mapper.cart_persistence_mapper import CartPersistenceMapper
from infrastructure.persistence.models.cart_model import Cart as CartModel, CartItem as CartItemModel


class CartRepositoryInterfaceImpl(CartRepositoryInterface):

    def get_active_cart(self, user_id: str) -> Optional[Cart]:
        model = CartModel.objects.filter(user_id=user_id, status='active', deleted_at__isnull=True).first()
        if not model:
            return None
        return CartPersistenceMapper.from_entity(model)

    def create_cart(self, user_id: str) -> Cart:
        model = CartModel.objects.create(user_id=user_id, status='active')
        return CartPersistenceMapper.from_entity(model)

    def get_item(self, cart_item_id: str, cart_id: str) -> Optional[CartItem]:
        model = CartItemModel.objects.filter(id=cart_item_id, cart_id=cart_id, deleted_at__isnull=True).first()
        return CartPersistenceMapper.item_from_entity(model)

    def find_existing_item(self, cart_id: str, product_id: str, variant_id: Optional[str]) -> Optional[CartItem]:
        model = CartItemModel.objects.filter(
            cart_id=cart_id,
            product_id=product_id,
            product_variant_id=variant_id,
            deleted_at__isnull=True,
        ).first()
        return CartPersistenceMapper.item_from_entity(model)

    def save_item(self, item: CartItem) -> CartItem:
        db_instance = CartItemModel.objects.filter(pk=item.id).first() if item.id else None
        db_instance = CartPersistenceMapper.item_to_model(item, db_instance)
        db_instance.save()
        return CartPersistenceMapper.item_from_entity(db_instance)

    def soft_delete_item(self, cart_item_id: str) -> None:
        from django.utils import timezone
        CartItemModel.objects.filter(id=cart_item_id).update(deleted_at=timezone.now())

    def select_all_items(self, cart_id: str, selected: bool) -> None:
        CartItemModel.objects.filter(cart_id=cart_id, deleted_at__isnull=True).update(is_selected=selected)

    def mark_checked_out(self, cart_id: str) -> None:
        CartModel.objects.filter(id=cart_id).update(status='checked_out')
