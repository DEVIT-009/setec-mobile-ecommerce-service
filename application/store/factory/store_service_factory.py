from application.store.store_service_facade import StoreServiceFacade
from domain.store.service.store_service import StoreServiceInterface
from infrastructure.persistence.repository.store_repository_impl import StoreRepositoryInterfaceImpl
from infrastructure.persistence.repository.product_repository_impl import ProductRepositoryInterfaceImpl


def store_service_factory() -> StoreServiceInterface:
    store_repo = StoreRepositoryInterfaceImpl()
    product_repo = ProductRepositoryInterfaceImpl()
    return StoreServiceFacade(store_repo=store_repo, product_repo=product_repo)
