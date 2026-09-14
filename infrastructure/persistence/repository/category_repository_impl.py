import uuid
from typing import List, Optional
from django.utils import timezone
from domain.category.ports.category_repository import CategoryRepositoryInterface
from domain.category.entity.category import Category
from domain.category.exception.category_exception import CategoryException
from infrastructure.persistence.mapper.category_persistence_mapper import CategoryPersistenceMapper
from infrastructure.persistence.models.category_model import Category as CategoryModel


def _is_uuid(val: str) -> bool:
    try:
        uuid.UUID(str(val))
        return True
    except (ValueError, AttributeError, TypeError):
        return False


class CategoryRepositoryInterfaceImpl(CategoryRepositoryInterface):

    def list_active(self, parent_id: Optional[str] = None) -> List[Category]:
        qs = CategoryModel.objects.filter(status='active', deleted_at__isnull=True)
        if parent_id:
            qs = qs.filter(parent_id=parent_id)
        else:
            qs = qs.filter(parent__isnull=True)
        models = qs.order_by('sort_order', 'name')
        return [CategoryPersistenceMapper.from_entity(m) for m in models if m is not None]

    def list_admin(self, parent_id: Optional[str] = None) -> List[Category]:
        """Return all non-deleted categories (active + inactive) for admin use."""
        qs = CategoryModel.objects.filter(deleted_at__isnull=True)
        if parent_id:
            qs = qs.filter(parent_id=parent_id)
        models = qs.order_by('sort_order', 'name')
        return [CategoryPersistenceMapper.from_entity(m) for m in models if m is not None]

    def get_by_slug(self, slug: str) -> Optional[Category]:
        model = CategoryModel.objects.filter(slug=slug, deleted_at__isnull=True).first()
        if not model:
            return None
        return CategoryPersistenceMapper.from_entity(model)

    def get_by_id(self, category_id: str) -> Optional[Category]:
        if not _is_uuid(category_id):
            return None
        model = CategoryModel.objects.filter(id=category_id, deleted_at__isnull=True).first()
        if not model:
            return None
        return CategoryPersistenceMapper.from_entity(model)

    def get_children(self, parent_id: str) -> List[Category]:
        models = CategoryModel.objects.filter(parent_id=parent_id, status='active', deleted_at__isnull=True).order_by('sort_order', 'name')
        return [CategoryPersistenceMapper.from_entity(m) for m in models if m is not None]

    def get_root_categories(self) -> List[Category]:
        models = CategoryModel.objects.filter(status='active', parent__isnull=True, deleted_at__isnull=True).order_by('sort_order', 'name')
        return [CategoryPersistenceMapper.from_entity(m) for m in models if m is not None]

    def exists_by_slug(self, slug: str, exclude_id: Optional[str] = None) -> bool:
        qs = CategoryModel.objects.filter(slug=slug, deleted_at__isnull=True)
        if exclude_id and _is_uuid(exclude_id):
            qs = qs.exclude(id=exclude_id)
        return qs.exists()

    def create(self, category: Category, actor_id: Optional[str] = None) -> Category:
        model = CategoryPersistenceMapper.to_model(category)
        if actor_id:
            model.created_by_id = actor_id
            model.updated_by_id = actor_id
        model.save()
        return CategoryPersistenceMapper.from_entity(model)

    def update(self, category: Category, actor_id: Optional[str] = None) -> Category:
        model = CategoryModel.objects.filter(id=category.id, deleted_at__isnull=True).first()
        if not model:
            raise CategoryException.not_found()
        model = CategoryPersistenceMapper.to_model(category, model)
        if actor_id:
            model.updated_by_id = actor_id
        model.save()
        return CategoryPersistenceMapper.from_entity(model)

    def soft_delete(self, category_id: str, actor_id: Optional[str] = None) -> None:
        qs = CategoryModel.objects.filter(deleted_at__isnull=True)
        if _is_uuid(category_id):
            model = qs.filter(id=category_id).first()
        else:
            model = qs.filter(slug=category_id).first()
        if not model:
            raise CategoryException.not_found()
        model.deleted_at = timezone.now()
        if actor_id:
            model.deleted_by_id = actor_id
        model.save()
