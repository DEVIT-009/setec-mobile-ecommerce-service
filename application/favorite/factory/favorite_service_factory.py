from application.favorite.favorite_service_facade import FavoriteServiceFacade
from domain.favorite.service.favorite_service import FavoriteServiceInterface
from infrastructure.persistence.repository.favorite_repository_impl import FavoriteRepositoryInterfaceImpl
from infrastructure.persistence.repository.product_repository_impl import ProductRepositoryInterfaceImpl


def favorite_service_factory() -> FavoriteServiceInterface:
    favorite_repo = FavoriteRepositoryInterfaceImpl()
    product_repo = ProductRepositoryInterfaceImpl()
    return FavoriteServiceFacade(favorite_repo=favorite_repo, product_repo=product_repo)
