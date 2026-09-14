from typing import Optional, Dict, Any, List
from domain.product.entity.product import Product
from domain.product.ports.product_repository import ProductRepositoryInterface
from domain.product.service.product_service import ProductServiceInterface
from domain.product.exception.product_exception import ProductException
from interface.product.serializer.mapper.product_controller_mapper import ProductControllerMapper


class ProductServiceFacade(ProductServiceInterface):

    def __init__(self, repo: ProductRepositoryInterface):
        self.repo = repo

    def list_active(self, filters: dict, page: int, page_size: int, user_id: Optional[str] = None) -> Dict[str, Any]:
        products, total = self.repo.list_active(filters, page, page_size, user_id)
        return {
            "items": ProductControllerMapper.to_card_list_response(products),
            "total": total,
        }

    def list_admin(self, filters: dict, page: int, page_size: int) -> Dict[str, Any]:
        products, total = self.repo.list_all(filters, page, page_size)
        return {
            "items": ProductControllerMapper.to_card_list_response(products),
            "total": total,
        }

    def get_by_id(self, product_id: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        product = self.repo.get_by_id(product_id, user_id)
        if not product:
            raise ProductException.not_found()
        return ProductControllerMapper.to_detail_response(product)

    def get_by_store_and_slug(self, store_slug: str, product_slug: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        product = self.repo.get_by_store_and_slug(store_slug, product_slug, user_id)
        if not product:
            raise ProductException.not_found()
        return ProductControllerMapper.to_detail_response(product)

    def get_images(self, product_id: str) -> List[Dict[str, Any]]:
        images = self.repo.get_images(product_id)
        return [ProductControllerMapper.image_to_response(i) for i in images]

    def get_variants(self, product_id: str) -> List[Dict[str, Any]]:
        variants = self.repo.get_variants(product_id)
        return [ProductControllerMapper.variant_to_response(v) for v in variants]

    def list_tags(self, page: int, page_size: int) -> Dict[str, Any]:
        tags, total = self.repo.list_tags(page, page_size)
        return {
            "items": [ProductControllerMapper.tag_to_response(t) for t in tags],
            "total": total,
        }

    def get_reviews(self, product_id: str, page: int, page_size: int) -> Dict[str, Any]:
        # Delegated to the review service — the facade does NOT query ORM directly.
        from application.review.factory.review_service_factory import review_service_factory
        review_service = review_service_factory()
        return review_service.list_public(product_id=product_id, page=page, page_size=page_size)


    def get_favorite_state(self, product_id: str, user_id: str) -> Dict[str, Any]:
        is_fav = self.repo.is_favorite(product_id, user_id)
        return {"product_id": str(product_id), "is_favorite": is_fav}

    def create(self, data: Dict[str, Any], actor_id: Optional[str] = None) -> Dict[str, Any]:
        store_id = data.get('store_id')
        slug = data.get('slug')

        if self.repo.exists_by_store_and_slug(store_id, slug):
            raise ProductException.already_exists(f"Product with slug '{slug}' already exists in this store")

        product = ProductControllerMapper.from_request(data)
        saved = self.repo.save(product, actor_id=actor_id)
        return ProductControllerMapper.to_card_response(saved)

    def update(self, product_id: str, data: Dict[str, Any], actor_id: Optional[str] = None, partial: bool = False) -> Dict[str, Any]:
        existing = self.repo.get_by_id(product_id)
        if not existing:
            raise ProductException.not_found()

        if 'slug' in data:
            new_slug = data['slug']
            if new_slug != existing.slug and existing.store_id:
                if self.repo.exists_by_store_and_slug(existing.store_id, new_slug, exclude_id=existing.id):
                    raise ProductException.already_exists(f"Product with slug '{new_slug}' already exists in this store")
            existing.slug = new_slug

        if not partial or 'name' in data:
            existing.name = data.get('name', existing.name)
        if not partial or 'description' in data:
            existing.description = data.get('description', existing.description)
        if not partial or 'base_price' in data:
            existing.base_price = float(data['base_price']) if 'base_price' in data else existing.base_price
        if not partial or 'compare_at_price' in data:
            existing.compare_at_price = float(data['compare_at_price']) if data.get('compare_at_price') is not None else (None if 'compare_at_price' in data else existing.compare_at_price)
        if not partial or 'currency' in data:
            existing.currency = data.get('currency', existing.currency)
        if not partial or 'sku' in data:
            existing.sku = data.get('sku', existing.sku)
        if not partial or 'status' in data:
            existing.status = data.get('status', existing.status)
        if not partial or 'category_id' in data:
            existing.category_id = data.get('category_id', existing.category_id)

        saved = self.repo.save(existing, actor_id=actor_id)
        return ProductControllerMapper.to_card_response(saved)

    def soft_delete(self, product_id: str, actor_id: Optional[str] = None) -> None:
        existing = self.repo.get_by_id(product_id)
        if not existing:
            raise ProductException.not_found()
        self.repo.soft_delete(existing.id, actor_id=actor_id)
