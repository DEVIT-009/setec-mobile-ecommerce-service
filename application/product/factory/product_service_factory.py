from application.product.product_service_facade import ProductServiceFacade
from domain.product.service.product_service import ProductServiceInterface
from infrastructure.persistence.repository.product_repository_impl import ProductRepositoryInterfaceImpl


def product_service_factory() -> ProductServiceInterface:
    repo = ProductRepositoryInterfaceImpl()
    return ProductServiceFacade(repo)
