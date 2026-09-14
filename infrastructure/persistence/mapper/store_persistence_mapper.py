from typing import Optional
from domain.store.entity.store import Store as DomainStore
from infrastructure.persistence.models.store_model import Store as StoreModel


class StorePersistenceMapper:

    @staticmethod
    def from_entity(entity: Optional[StoreModel]) -> Optional[DomainStore]:
        if entity is None:
            return None
        return DomainStore(
            id=str(entity.id),
            owner_id=str(entity.owner_id) if entity.owner_id else None,
            name=entity.name,
            slug=entity.slug,
            description=entity.description,
            logo_url=entity.logo_url,
            banner_url=entity.banner_url,
            status=entity.status,
            rating_average=float(entity.rating_average) if entity.rating_average is not None else 0.0,
            rating_count=entity.rating_count,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )

    @staticmethod
    def to_model(domain: DomainStore, model_instance: Optional[StoreModel] = None) -> StoreModel:
        model = model_instance or StoreModel()
        if domain.owner_id:
            model.owner_id = domain.owner_id
        model.name = domain.name
        model.slug = domain.slug
        model.description = domain.description
        model.logo_url = domain.logo_url
        model.banner_url = domain.banner_url
        model.status = domain.status
        model.deleted_at = domain.deleted_at
        return model
