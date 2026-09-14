from application.search_history.search_history_service_facade import SearchHistoryServiceFacade
from domain.search_history.service.search_service import SearchServiceInterface
from infrastructure.persistence.repository.search_repository_impl import SearchRepositoryInterfaceImpl


def search_history_service_factory() -> SearchServiceInterface:
    repo = SearchRepositoryInterfaceImpl()
    return SearchHistoryServiceFacade(repo)
