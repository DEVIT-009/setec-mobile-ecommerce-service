from typing import Dict, Any, List
from dataclasses import asdict
from domain.category.entity.category import Category
from interface.category.serializer.response.category_response import CategoryResponse


class CategoryControllerMapper:

    @staticmethod
    def from_request(validated_data: Dict[str, Any]) -> Category:
        return Category(
            parent_id=validated_data.get("parent_id"),
            name=validated_data.get("name", ""),
            slug=validated_data.get("slug", ""),
            icon_url=validated_data.get("icon_url"),
            image_url=validated_data.get("image_url"),
            sort_order=validated_data.get("sort_order", 0),
            status=validated_data.get("status", "active"),
        )

    @staticmethod
    def to_response(category: Category) -> Dict[str, Any]:
        response_dto = CategoryResponse(
            id=str(category.id) if category.id else None,
            parent_id=str(category.parent_id) if category.parent_id else None,
            name=category.name,
            slug=category.slug,
            icon_url=category.icon_url,
            image_url=category.image_url,
            sort_order=category.sort_order,
            status=category.status,
        )
        return asdict(response_dto)

    @staticmethod
    def to_list_response(categories: List[Category]) -> List[Dict[str, Any]]:
        return [CategoryControllerMapper.to_response(c) for c in categories]

    @staticmethod
    def to_response_with_products(category: Category, products: List[Any]) -> Dict[str, Any]:
        category_dict = CategoryControllerMapper.to_response(category)
        category_dict["product"] = [
            CategoryControllerMapper.to_category_product_item(p) for p in products
        ]
        return category_dict

    @staticmethod
    def to_category_product_item(product: Any) -> Dict[str, Any]:
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

