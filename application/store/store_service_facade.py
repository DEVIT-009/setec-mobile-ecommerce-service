from typing import Dict, Any, Optional
from domain.store.entity.store import Store
from domain.store.ports.store_repository import StoreRepositoryInterface
from domain.store.service.store_service import StoreServiceInterface
from domain.store.exception.store_exception import StoreException
from domain.product.ports.product_repository import ProductRepositoryInterface
from interface.store.serializer.mapper.store_controller_mapper import StoreControllerMapper
from interface.product.serializer.mapper.product_controller_mapper import ProductControllerMapper


class StoreServiceFacade(StoreServiceInterface):

    def __init__(self, store_repo: StoreRepositoryInterface, product_repo: ProductRepositoryInterface):
        self.store_repo = store_repo
        self.product_repo = product_repo

    def list_active(self, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        stores, total = self.store_repo.list_active(page, page_size)
        return {
            "items": StoreControllerMapper.to_list_response(stores),
            "total": total,
        }

    def list_admin(self, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        stores, total = self.store_repo.list_all(page, page_size)
        return {
            "items": StoreControllerMapper.to_list_response(stores),
            "total": total,
        }

    def get_by_id(self, store_id: str) -> Dict[str, Any]:
        store = self.store_repo.get_by_id(store_id)
        if not store:
            raise StoreException.not_found()
        return StoreControllerMapper.to_response(store)

    def get_by_slug(self, slug: str) -> Dict[str, Any]:
        store = self.store_repo.get_by_slug(slug)
        if not store:
            raise StoreException.not_found()
        return StoreControllerMapper.to_response(store)

    def _find_admin(self, identifier: str) -> Store:
        store = self.store_repo.get_by_id(identifier)
        if not store:
            store = self.store_repo.get_by_slug(identifier)
        if not store:
            raise StoreException.not_found()
        return store

    def get_admin(self, identifier: str) -> Dict[str, Any]:
        store = self._find_admin(identifier)
        return StoreControllerMapper.to_response(store)

    def list_products(self, store_id: str, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        store = self.store_repo.get_by_id(store_id)
        if not store:
            store = self.store_repo.get_by_slug(store_id)
        if not store:
            raise StoreException.not_found()

        products, total = self.product_repo.list_active(filters={'store_id': store.id}, page=page, page_size=page_size)
        return {
            "items": ProductControllerMapper.to_card_list_response(products),
            "total": total,
        }

    def list_products_by_slug(self, slug: str, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        store = self.store_repo.get_by_slug(slug)
        if not store:
            raise StoreException.not_found()

        products, total = self.product_repo.list_active(filters={'store_id': store.id}, page=page, page_size=page_size)
        return {
            "items": ProductControllerMapper.to_card_list_response(products),
            "total": total,
        }

    def create(self, data: Dict[str, Any], actor_id: Optional[str] = None) -> Dict[str, Any]:
        slug = data.get('slug')
        if not slug:
            raise StoreException.already_exists("Store slug is required")
        if self.store_repo.exists_by_slug(slug):
            raise StoreException.already_exists(f"Store with slug '{slug}' already exists")

        store = StoreControllerMapper.from_request(data)
        if not store.owner_id and actor_id:
            store.owner_id = actor_id

        saved = self.store_repo.create(store, actor_id=actor_id)
        return StoreControllerMapper.to_response(saved)

    def update(self, store_id: str, data: Dict[str, Any], partial: bool = False, actor_id: Optional[str] = None) -> Dict[str, Any]:
        existing = self.store_repo.get_by_id(store_id)
        if not existing:
            existing = self.store_repo.get_by_slug(store_id)
        if not existing:
            raise StoreException.not_found()

        new_slug = data.get('slug')
        if new_slug and new_slug != existing.slug:
            if self.store_repo.exists_by_slug(new_slug, exclude_id=existing.id):
                raise StoreException.already_exists(f"Store with slug '{new_slug}' already exists")
            existing.slug = new_slug

        if 'name' in data or not partial:
            if 'name' in data:
                existing.name = data['name']
        if 'description' in data or not partial:
            if 'description' in data:
                existing.description = data['description']
        if 'logo_url' in data or not partial:
            if 'logo_url' in data:
                existing.logo_url = data['logo_url']
        if 'banner_url' in data or not partial:
            if 'banner_url' in data:
                existing.banner_url = data['banner_url']
        if 'status' in data or not partial:
            if 'status' in data:
                existing.status = data['status']
        if 'owner_id' in data:
            existing.owner_id = data['owner_id']

        saved = self.store_repo.update(existing, actor_id=actor_id)
        return StoreControllerMapper.to_response(saved)

    def soft_delete(self, store_id: str, actor_id: Optional[str] = None) -> None:
        existing = self.store_repo.get_by_id(store_id)
        if not existing:
            existing = self.store_repo.get_by_slug(store_id)
        if not existing:
            raise StoreException.not_found()
        self.store_repo.soft_delete(existing.id, actor_id=actor_id)
