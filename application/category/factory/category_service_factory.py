from application.category.category_service_facade import CategoryServiceFacade
from domain.category.service.category_service import CategoryServiceInterface
from infrastructure.persistence.repository.category_repository_impl import CategoryRepositoryInterfaceImpl
from infrastructure.persistence.repository.product_repository_impl import ProductRepositoryInterfaceImpl


def category_service_factory() -> CategoryServiceInterface:
    repo = CategoryRepositoryInterfaceImpl()
    product_repo = ProductRepositoryInterfaceImpl()
    return CategoryServiceFacade(repo=repo, product_repo=product_repo)
