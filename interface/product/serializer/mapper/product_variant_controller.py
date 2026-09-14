from typing import List, Dict, Any, Optional
from dataclasses import asdict
from domain.product.entity.product import ProductVariant, VariantOption
from interface.product.serializer.response.product_variant_response import (
    ProductVariantDetailResponse,
    VariantOptionResponse,
)


class ProductVariantControllerMapper:

    @staticmethod
    def from_request(validated_data: Dict[str, Any]) -> ProductVariant:
        """Convert validated request dict → Domain Entity."""
        options = [
            VariantOption(name=o['name'], value=o['value'])
            for o in validated_data.get('options', [])
        ]
        return ProductVariant(
            product_id=str(validated_data.get('product_id', '')),
            name=validated_data.get('name', ''),
            sku=validated_data.get('sku'),
            price=float(validated_data['price']) if validated_data.get('price') is not None else None,
            stock_quantity=validated_data.get('stock_quantity', 0),
            status=validated_data.get('status', 'active'),
            options=options,
        )

    @staticmethod
    def option_to_response(o: VariantOption) -> Dict[str, Any]:
        return asdict(VariantOptionResponse(name=o.name, value=o.value))

    @staticmethod
    def to_detail_response(v: ProductVariant) -> Dict[str, Any]:
        response_dto = ProductVariantDetailResponse(
            id=str(v.id) if v.id else None,
            product_id=str(v.product_id) if v.product_id else None,
            name=v.name,
            sku=v.sku,
            price=str(v.price) if v.price is not None else None,
            stock_quantity=v.stock_quantity,
            status=v.status,
            options=[ProductVariantControllerMapper.option_to_response(o) for o in v.options],
        )
        return asdict(response_dto)

    @staticmethod
    def to_list_response(variants: List[ProductVariant]) -> List[Dict[str, Any]]:
        return [ProductVariantControllerMapper.to_detail_response(v) for v in variants]
