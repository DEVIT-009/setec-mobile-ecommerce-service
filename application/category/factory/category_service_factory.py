from application.category.category_service_facade import CategoryServiceFacade
from domain.category.service.category_service import CategoryServiceInterface
from infrastructure.persistence.repository.category_repository_impl import CategoryRepositoryInterfaceImpl


def category_service_factory() -> CategoryServiceInterface:
    repo = CategoryRepositoryInterfaceImpl()
    return CategoryServiceFacade(repo)
