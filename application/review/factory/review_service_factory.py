from application.review.review_service_facade import ReviewServiceFacade
from domain.review.service.review_service import ReviewServiceInterface
from infrastructure.persistence.repository.review_repository_impl import ReviewRepositoryInterfaceImpl


def review_service_factory() -> ReviewServiceInterface:
    repo = ReviewRepositoryInterfaceImpl()
    return ReviewServiceFacade(repo)
