from decimal import Decimal
from typing import Optional, List
from domain.cart.entity.cart import Cart as DomainCart, CartItem as DomainCartItem, CartTotals as DomainCartTotals
from infrastructure.persistence.models.cart_model import Cart as CartModel, CartItem as CartItemModel


class CartPersistenceMapper:

    @staticmethod
    def item_from_entity(entity: Optional[CartItemModel]) -> Optional[DomainCartItem]:
        if entity is None:
            return None
        
        # Primary image URL if product loaded
        primary_image = None
        if getattr(entity, 'product', None):
            primary = entity.product.images.filter(is_primary=True, deleted_at__isnull=True).first()
            primary_image = primary.image_url if primary else None

        return DomainCartItem(
            id=str(entity.id),
            cart_id=str(entity.cart_id) if entity.cart_id else None,
            product_id=str(entity.product_id) if entity.product_id else None,
            product_name=entity.product.name if getattr(entity, 'product', None) else None,
            primary_image_url=primary_image,
            product_variant_id=str(entity.product_variant_id) if entity.product_variant_id else None,
            variant_name=entity.product_variant.name if getattr(entity, 'product_variant', None) else None,
            quantity=entity.quantity,
            unit_price_snapshot=Decimal(str(entity.unit_price_snapshot)),
            is_selected=entity.is_selected,
            deleted_at=entity.deleted_at,
        )

    @staticmethod
    def item_to_model(domain: DomainCartItem, model_instance: Optional[CartItemModel] = None) -> CartItemModel:
        model = model_instance or CartItemModel()
        if domain.cart_id:
            model.cart_id = domain.cart_id
        if domain.product_id:
            model.product_id = domain.product_id
        if domain.product_variant_id:
            model.product_variant_id = domain.product_variant_id
        model.quantity = domain.quantity
        model.unit_price_snapshot = domain.unit_price_snapshot
        model.is_selected = domain.is_selected
        return model

    @staticmethod
    def from_entity(entity: Optional[CartModel]) -> Optional[DomainCart]:
        if entity is None:
            return None
        
        items = []
        if hasattr(entity, 'items'):
            active_items = entity.items.filter(deleted_at__isnull=True).select_related('product', 'product_variant').prefetch_related('product__images')
            items = [CartPersistenceMapper.item_from_entity(item) for item in active_items if item is not None]

        selected_items = [i for i in items if i.is_selected]
        selected_count = sum(i.quantity for i in selected_items)
        subtotal = sum(i.unit_price_snapshot * i.quantity for i in selected_items)
        totals = DomainCartTotals(
            selected_item_count=selected_count,
            subtotal_amount=subtotal,
            shipping_amount=Decimal("0.00"),
            discount_amount=Decimal("0.00"),
            tax_amount=Decimal("0.00"),
            total_amount=subtotal,
            currency="USD",
        )

        return DomainCart(
            id=str(entity.id),
            user_id=str(entity.user_id) if entity.user_id else None,
            status=entity.status,
            items=items,
            totals=totals,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
