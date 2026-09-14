from application.auth.auth_service_facade import AuthServiceFacade
from domain.auth.service.auth_service import AuthServiceInterface
from infrastructure.persistence.repository.user_repository_impl import UserRepositoryInterfaceImpl


def auth_service_factory() -> AuthServiceInterface:
    repo = UserRepositoryInterfaceImpl()
    return AuthServiceFacade(user_repo=repo)
