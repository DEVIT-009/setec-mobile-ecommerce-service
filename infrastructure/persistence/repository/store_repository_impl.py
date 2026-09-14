import uuid
from typing import Optional, List, Tuple
from django.utils import timezone
from domain.store.ports.store_repository import StoreRepositoryInterface
from domain.store.entity.store import Store
from domain.store.exception.store_exception import StoreException
from infrastructure.persistence.mapper.store_persistence_mapper import StorePersistenceMapper
from infrastructure.persistence.models.store_model import Store as StoreModel


def _is_uuid(val: str) -> bool:
    try:
        uuid.UUID(str(val))
        return True
    except (ValueError, AttributeError, TypeError):
        return False


class StoreRepositoryInterfaceImpl(StoreRepositoryInterface):

    def list_active(self, page: int = 1, page_size: int = 20) -> Tuple[List[Store], int]:
        qs = StoreModel.objects.filter(status='active', deleted_at__isnull=True).order_by('name')
        total = qs.count()
        offset = (page - 1) * page_size
        models = list(qs[offset:offset + page_size])
        return [StorePersistenceMapper.from_entity(m) for m in models if m is not None], total

    def list_all(self, page: int = 1, page_size: int = 20) -> Tuple[List[Store], int]:
        qs = StoreModel.objects.filter(deleted_at__isnull=True).order_by('name')
        total = qs.count()
        offset = (page - 1) * page_size
        models = list(qs[offset:offset + page_size])
        return [StorePersistenceMapper.from_entity(m) for m in models if m is not None], total

    def get_by_slug(self, slug: str) -> Optional[Store]:
        model = StoreModel.objects.filter(slug=slug, deleted_at__isnull=True).first()
        if not model:
            return None
        return StorePersistenceMapper.from_entity(model)

    def get_by_id(self, store_id: str) -> Optional[Store]:
        if not _is_uuid(store_id):
            return None
        model = StoreModel.objects.filter(id=store_id, deleted_at__isnull=True).first()
        if not model:
            return None
        return StorePersistenceMapper.from_entity(model)

    def exists_by_slug(self, slug: str, exclude_id: Optional[str] = None) -> bool:
        qs = StoreModel.objects.filter(slug=slug, deleted_at__isnull=True)
        if exclude_id and _is_uuid(exclude_id):
            qs = qs.exclude(id=exclude_id)
        return qs.exists()

    def create(self, store: Store, actor_id: Optional[str] = None) -> Store:
        model = StorePersistenceMapper.to_model(store)
        if actor_id and _is_uuid(actor_id):
            model.created_by_id = actor_id
            model.updated_by_id = actor_id
        model.save()
        return StorePersistenceMapper.from_entity(model)

    def update(self, store: Store, actor_id: Optional[str] = None) -> Store:
        model = StoreModel.objects.filter(id=store.id, deleted_at__isnull=True).first()
        if not model:
            raise StoreException.not_found()
        model = StorePersistenceMapper.to_model(store, model)
        if actor_id and _is_uuid(actor_id):
            model.updated_by_id = actor_id
        model.save()
        return StorePersistenceMapper.from_entity(model)

    def soft_delete(self, store_id: str, actor_id: Optional[str] = None) -> None:
        qs = StoreModel.objects.filter(deleted_at__isnull=True)
        if _is_uuid(store_id):
            model = qs.filter(id=store_id).first()
        else:
            model = qs.filter(slug=store_id).first()
        if not model:
            raise StoreException.not_found()
        model.deleted_at = timezone.now()
        if actor_id and _is_uuid(actor_id):
            model.deleted_by_id = actor_id
        model.save()

    def save(self, store: Store, actor_id: Optional[str] = None) -> Store:
        if store.id and _is_uuid(store.id):
            existing = StoreModel.objects.filter(id=store.id, deleted_at__isnull=True).first()
            if existing:
                return self.update(store, actor_id)
        return self.create(store, actor_id)
