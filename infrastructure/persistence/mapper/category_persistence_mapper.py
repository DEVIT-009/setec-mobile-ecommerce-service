from typing import Optional
from domain.category.entity.category import Category
from infrastructure.persistence.models.category_model import Category as CategoryModel


class CategoryPersistenceMapper:

    @staticmethod
    def from_entity(entity: Optional[CategoryModel]) -> Optional[Category]:
        if entity is None:
            return None
        return Category(
            id=str(entity.id),
            parent_id=str(entity.parent_id) if entity.parent_id else None,
            name=entity.name,
            slug=entity.slug,
            icon_url=entity.icon_url,
            image_url=entity.image_url,
            sort_order=entity.sort_order,
            status=entity.status,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )

    @staticmethod
    def to_model(domain: Category, model_instance: Optional[CategoryModel] = None) -> CategoryModel:
        model = model_instance or CategoryModel()
        if domain.parent_id:
            model.parent_id = domain.parent_id
        model.name = domain.name
        model.slug = domain.slug
        model.icon_url = domain.icon_url
        model.image_url = domain.image_url
        model.sort_order = domain.sort_order
        model.status = domain.status
        model.deleted_at = domain.deleted_at
        return model
