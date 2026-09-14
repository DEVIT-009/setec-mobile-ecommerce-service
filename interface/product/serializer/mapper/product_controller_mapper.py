from typing import List, Dict, Any, Optional
from dataclasses import asdict
from domain.product.entity.product import Product, ProductImage, ProductVariant, Tag
from interface.product.serializer.response.product_response import (
    ProductCardResponse,
    ProductDetailResponse,
    ProductImageResponse,
    ProductVariantResponse,
    TagResponse,
)


class ProductControllerMapper:

    @staticmethod
    def from_request(validated_data: Dict[str, Any]) -> Product:
        """Convert validated request dict → Domain Entity."""
        return Product(
            store_id=validated_data.get('store_id'),
            category_id=validated_data.get('category_id'),
            name=validated_data.get('name', ''),
            slug=validated_data.get('slug', ''),
            description=validated_data.get('description'),
            base_price=float(validated_data.get('base_price', 0)),
            compare_at_price=float(validated_data['compare_at_price']) if validated_data.get('compare_at_price') is not None else None,
            currency=validated_data.get('currency', 'USD'),
            sku=validated_data.get('sku'),
            status=validated_data.get('status', 'draft'),
        )

    @staticmethod
    def to_card_response(p: Product) -> Dict[str, Any]:
        response_dto = ProductCardResponse(
            id=str(p.id) if p.id else None,
            name=p.name,
            slug=p.slug,
            base_price=str(p.base_price),
            compare_at_price=str(p.compare_at_price) if p.compare_at_price is not None else None,
            currency=p.currency,
            primary_image_url=p.primary_image_url,
            rating_average=p.rating_average,
            rating_count=p.rating_count,
            sold_count=p.sold_count,
            status=p.status,
            store={"id": p.store_id, "name": p.store_name, "slug": p.store_slug} if p.store_id else None,
            is_favorite=p.is_favorite,
        )
        return asdict(response_dto)

    @staticmethod
    def to_detail_response(p: Product) -> Dict[str, Any]:
        response_dto = ProductDetailResponse(
            id=str(p.id) if p.id else None,
            name=p.name,
            slug=p.slug,
            base_price=str(p.base_price),
            compare_at_price=str(p.compare_at_price) if p.compare_at_price is not None else None,
            currency=p.currency,
            primary_image_url=p.primary_image_url,
            rating_average=p.rating_average,
            rating_count=p.rating_count,
            sold_count=p.sold_count,
            status=p.status,
            store={"id": p.store_id, "name": p.store_name, "slug": p.store_slug} if p.store_id else None,
            is_favorite=p.is_favorite,
            description=p.description,
            sku=p.sku,
            category={"id": p.category_id, "name": p.category_name, "slug": None} if p.category_id else None,
            images=[ProductControllerMapper.image_to_response(i) for i in p.images],
            variants=[ProductControllerMapper.variant_to_response(v) for v in p.variants],
            tags=[ProductControllerMapper.tag_to_response(t) for t in p.tags],
        )
        return asdict(response_dto)

    @staticmethod
    def image_to_response(i: ProductImage) -> Dict[str, Any]:
        response_dto = ProductImageResponse(
            id=str(i.id) if i.id else None,
            image_url=i.image_url,
            alt_text=i.alt_text,
            sort_order=i.sort_order,
            is_primary=i.is_primary,
        )
        return asdict(response_dto)

    @staticmethod
    def variant_to_response(v: ProductVariant) -> Dict[str, Any]:
        response_dto = ProductVariantResponse(
            id=str(v.id) if v.id else None,
            name=v.name,
            sku=v.sku,
            price=str(v.price) if v.price is not None else None,
            stock_quantity=v.stock_quantity,
            status=v.status,
            options=[{"name": o.name, "value": o.value} for o in v.options],
        )
        return asdict(response_dto)

    @staticmethod
    def tag_to_response(t: Tag) -> Dict[str, Any]:
        response_dto = TagResponse(
            id=str(t.id) if t.id else None,
            name=t.name,
            slug=t.slug,
        )
        return asdict(response_dto)

    @staticmethod
    def to_card_list_response(products: List[Product]) -> List[Dict[str, Any]]:
        return [ProductControllerMapper.to_card_response(p) for p in products]

