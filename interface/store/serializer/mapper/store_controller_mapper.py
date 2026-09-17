from typing import Dict, Any, List
from dataclasses import asdict
from domain.store.entity.store import Store
from interface.store.serializer.response.store_response import StoreResponse


class StoreControllerMapper:

    @staticmethod
    def from_request(validated_data: Dict[str, Any]) -> Store:
        return Store(
            owner_id=validated_data.get("owner_id"),
            name=validated_data.get("name", ""),
            slug=validated_data.get("slug", ""),
            description=validated_data.get("description"),
            logo_url=validated_data.get("logo_url"),
            banner_url=validated_data.get("banner_url"),
            status=validated_data.get("status", "active"),
        )

    @staticmethod
    def to_response(store: Store) -> Dict[str, Any]:
        response_dto = StoreResponse(
            id=str(store.id) if store.id else None,
            owner_id=str(store.owner_id) if store.owner_id else None,
            name=store.name,
            slug=store.slug,
            description=store.description,
            logo_url=store.logo_url,
            banner_url=store.banner_url,
            status=store.status,
            rating_average=store.rating_average,
            rating_count=store.rating_count,
            created_at=store.created_at.isoformat() if store.created_at else None,
        )
        return asdict(response_dto)

    @staticmethod
    def to_list_response(stores: List[Store]) -> List[Dict[str, Any]]:
        return [StoreControllerMapper.to_response(s) for s in stores]

    @staticmethod
    def to_store_product_item(product: Any) -> Dict[str, Any]:
        return {
            "id": str(product.id) if product.id else None,
            "name": product.name,
            "slug": product.slug,
            "base_price": str(product.base_price),
            "currency": product.currency,
            "rating_average": product.rating_average,
            "rating_count": product.rating_count,
            "sold_count": product.sold_count,
            "compare_at_price": str(product.compare_at_price) if product.compare_at_price is not None else None,
            "primary_image_url": product.primary_image_url,
            "is_favorite": getattr(product, "is_favorite", False),
        }

    @staticmethod
    def to_response_with_products(store: Store, products: List[Any]) -> Dict[str, Any]:
        store_dict = StoreControllerMapper.to_response(store)
        store_dict["product"] = [
            StoreControllerMapper.to_store_product_item(p) for p in products
        ]
        return store_dict
