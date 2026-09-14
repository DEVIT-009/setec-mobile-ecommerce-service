from typing import Dict, Any
from dataclasses import asdict
from domain.cart.entity.cart import Cart, CartItem
from interface.cart.serializer.response.cart_response import (
    CartResponse,
    CartItemResponse,
    CartTotalsResponse,
)


class CartControllerMapper:

    @staticmethod
    def item_to_response(item: CartItem) -> Dict[str, Any]:
        response_dto = CartItemResponse(
            id=str(item.id) if item.id else None,
            product={
                "id": item.product_id,
                "name": item.product_name,
                "primary_image_url": item.primary_image_url,
            },
            variant={
                "id": item.product_variant_id,
                "name": item.variant_name,
            } if item.product_variant_id else None,
            quantity=item.quantity,
            unit_price_snapshot=str(item.unit_price_snapshot),
            line_total=str(item.unit_price_snapshot * item.quantity),
            is_selected=item.is_selected,
        )
        return asdict(response_dto)

    @staticmethod
    def to_response(cart: Cart) -> Dict[str, Any]:
        totals_dto = CartTotalsResponse(
            selected_item_count=cart.totals.selected_item_count if cart.totals else 0,
            subtotal_amount=str(cart.totals.subtotal_amount) if cart.totals else "0.00",
            shipping_amount=str(cart.totals.shipping_amount) if cart.totals else "0.00",
            discount_amount=str(cart.totals.discount_amount) if cart.totals else "0.00",
            tax_amount=str(cart.totals.tax_amount) if cart.totals else "0.00",
            total_amount=str(cart.totals.total_amount) if cart.totals else "0.00",
            currency=cart.totals.currency if cart.totals else "USD",
        )
        response_dto = CartResponse(
            id=str(cart.id) if cart.id else None,
            status=cart.status,
            items=[CartControllerMapper.item_to_response(i) for i in cart.items],
            totals=asdict(totals_dto),
        )
        return asdict(response_dto)

