from typing import Optional, List, Tuple
from django.utils import timezone
from domain.favorite.ports.favorite_repository import FavoriteRepositoryInterface
from domain.favorite.entity.favorite import Favorite
from infrastructure.persistence.mapper.favorite_persistence_mapper import FavoritePersistenceMapper
from infrastructure.persistence.models.favorite_model import Favorite as FavoriteModel


class FavoriteRepositoryInterfaceImpl(FavoriteRepositoryInterface):

    def list_by_user(self, user_id: str, page: int, page_size: int) -> Tuple[List[Favorite], int]:
        qs = FavoriteModel.objects.filter(user_id=user_id, deleted_at__isnull=True).order_by('-created_at')
        total = qs.count()
        offset = (page - 1) * page_size
        models = list(qs[offset:offset + page_size])
        return [FavoritePersistenceMapper.from_entity(m) for m in models if m is not None], total

    def get(self, user_id: str, product_id: str) -> Optional[Favorite]:
        model = FavoriteModel.objects.filter(user_id=user_id, product_id=product_id, deleted_at__isnull=True).first()
        if not model:
            return None
        return FavoritePersistenceMapper.from_entity(model)

    def save(self, favorite: Favorite) -> Favorite:
        db_instance = FavoriteModel.objects.filter(pk=favorite.id).first() if favorite.id else None
        db_instance = FavoritePersistenceMapper.to_model(favorite, db_instance)
        db_instance.save()
        return FavoritePersistenceMapper.from_entity(db_instance)

    def remove(self, user_id: str, product_id: str) -> bool:
        fav = FavoriteModel.objects.filter(user_id=user_id, product_id=product_id, deleted_at__isnull=True).first()
        if fav:
            fav.deleted_at = timezone.now()
            fav.save()
            return True
        return False
