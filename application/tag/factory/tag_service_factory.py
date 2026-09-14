from application.tag.tag_service_facade import TagServiceFacade
from domain.tag.service.tag_service import TagServiceInterface
from infrastructure.persistence.repository.tag_repository_impl import TagRepositoryImpl


def tag_service_factory() -> TagServiceInterface:
    repo = TagRepositoryImpl()
    return TagServiceFacade(repo)
