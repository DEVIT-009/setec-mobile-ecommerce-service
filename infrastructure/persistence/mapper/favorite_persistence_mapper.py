from typing import Optional
from domain.favorite.entity.favorite import Favorite as DomainFavorite
from infrastructure.persistence.models.favorite_model import Favorite as FavoriteModel


class FavoritePersistenceMapper:

    @staticmethod
    def from_entity(entity: Optional[FavoriteModel]) -> Optional[DomainFavorite]:
        if entity is None:
            return None
        return DomainFavorite(
            id=str(entity.id),
            user_id=str(entity.user_id) if entity.user_id else None,
            product_id=str(entity.product_id) if entity.product_id else None,
            created_at=entity.created_at,
            deleted_at=entity.deleted_at,
        )

    @staticmethod
    def to_model(domain: DomainFavorite, model_instance: Optional[FavoriteModel] = None) -> FavoriteModel:
        model = model_instance or FavoriteModel()
        if domain.user_id:
            model.user_id = domain.user_id
        if domain.product_id:
            model.product_id = domain.product_id
        model.deleted_at = domain.deleted_at
        return model
