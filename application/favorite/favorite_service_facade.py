from typing import Dict, Any
from domain.favorite.ports.favorite_repository import FavoriteRepositoryInterface
from domain.favorite.service.favorite_service import FavoriteServiceInterface
from domain.favorite.entity.favorite import Favorite
from domain.product.ports.product_repository import ProductRepositoryInterface
from interface.product.serializer.mapper.product_controller_mapper import ProductControllerMapper


class FavoriteServiceFacade(FavoriteServiceInterface):

    def __init__(self, favorite_repo: FavoriteRepositoryInterface, product_repo: ProductRepositoryInterface):
        self.favorite_repo = favorite_repo
        self.product_repo = product_repo

    def list(self, user_id: str, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        favorites, total = self.favorite_repo.list_by_user(user_id, page, page_size)
        items = []
        for fav in favorites:
            p = self.product_repo.get_by_id(fav.product_id, user_id=user_id)
            if p:
                items.append(ProductControllerMapper.to_card_response(p))
        return {"items": items, "total": total}

    def add(self, user_id: str, product_id: str) -> Dict[str, Any]:
        existing = self.favorite_repo.get(user_id, product_id)
        if not existing:
            fav = Favorite(user_id=user_id, product_id=product_id)
            self.favorite_repo.save(fav)
        return {"product_id": product_id, "is_favorite": True}

    def remove(self, user_id: str, product_id: str) -> None:
        self.favorite_repo.remove(user_id, product_id)

    def get_state(self, user_id: str, product_id: str) -> Dict[str, Any]:
        fav = self.favorite_repo.get(user_id, product_id)
        return {"product_id": product_id, "is_favorite": fav is not None}
