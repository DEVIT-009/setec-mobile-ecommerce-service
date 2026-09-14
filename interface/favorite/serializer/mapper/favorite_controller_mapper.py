from typing import Dict, Any, List
from dataclasses import asdict
from domain.favorite.entity.favorite import Favorite
from interface.favorite.serializer.response.favorite_response import FavoriteResponse


class FavoriteControllerMapper:

    @staticmethod
    def to_response(favorite: Favorite) -> Dict[str, Any]:
        response_dto = FavoriteResponse(
            id=str(favorite.id) if favorite.id else None,
            user_id=str(favorite.user_id) if favorite.user_id else None,
            product_id=str(favorite.product_id) if favorite.product_id else None,
            created_at=favorite.created_at.isoformat() if favorite.created_at else None,
        )
        return asdict(response_dto)

    @staticmethod
    def to_list_response(favorites: List[Favorite]) -> List[Dict[str, Any]]:
        return [FavoriteControllerMapper.to_response(f) for f in favorites]

